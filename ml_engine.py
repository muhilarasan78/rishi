import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import os
import numpy as np
import random
from api_manager import TripGenixAPIManager

class RecommendationEngine:
    """
    TripGenix Recommendation Engine (KNN Powered)
    Uses TF-IDF Vectorization and K-Nearest Neighbors to find similar destinations.
    """
    def __init__(self, data_path="tourism_data.csv"):
        # Ensure data exists; if not, generate it (which also enriches it)
        if not os.path.exists(data_path):
            import data_generator
            data_generator.generate_data()
            
        self.df = pd.read_csv(data_path)
        
        # Ensure Combined_Features exists (backward compatibility or regeneration)
        if 'Combined_Features' not in self.df.columns:
            # Fallback creation if for some reason csv is old
            self.df['Combined_Features'] = (
                self.df['Category'].fillna('') + " " + 
                self.df['Activities'].fillna('') + " " + 
                self.df['Budget'].fillna('') + " " + 
                self.df['State'].fillna('')
            )

        self._initialize_ml()
        self.api_manager = TripGenixAPIManager()

    def _initialize_ml(self):
        """
        Train the KNN Model:
        1. Vectorize 'Combined_Features' using TF-IDF.
        2. Fit NearestNeighbors model on the vectors.
        """
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['Combined_Features'].fillna(''))
        
        # KNN Model
        # Metric: cosine distance (1 - cosine similarity)
        # Algorithm: brute is good for smaller datasets, auto works generally
        self.knn = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute')
        self.knn.fit(self.tfidf_matrix)

    def get_recommendations(self, state, district, budget, interests, days=3):
        """
        KNN-based recommendation:
        1. Create a query vector from user inputs.
        2. Find K-nearest neighbors.
        3. Rank and filter results.
        """
        
        # 1. Construct User Query
        # "Beach Relaxing Low Kerala"
        query_text = f"{interests} {budget} {state if state != 'All' else ''} {district if district != 'All' else ''}"
        query_vec = self.tfidf.transform([query_text])
        
        # 2. Find Neighbors
        # Returns distances and indices of the nearest neighbors
        # We ask for more than we need (e.g., 20) to allow for post-filtering
        n_neighbors = min(20, len(self.df))
        distances, indices = self.knn.kneighbors(query_vec, n_neighbors=n_neighbors)
        
        # 3. Process Results
        candidates = self.df.iloc[indices[0]].copy()
        candidates['distance'] = distances[0]
        # Convert distance to similarity score (1 - distance) for display
        candidates['score'] = 1 - candidates['distance']
        
        # 4. Apply Hard/Soft Filters
        # Even though KNN finds "similar" items, we might want to strictly enforce budget if user desires.
        # However, prompts say "Recommendation", so maybe just rank them.
        # Let's strictly filter budget if provided, as that's a hard constraint for many.
        if budget:
             candidates = candidates[candidates['Budget'].str.lower() == budget.lower()]
             
        # If no candidates left after filtering, revert to top KNN results (soft filter fallback)
        if candidates.empty:
            candidates = self.df.iloc[indices[0]].copy()
            candidates['distance'] = distances[0]
            candidates['score'] = 1 - candidates['distance']

        # 5. Select Top Results
        top_results = candidates.head(5).to_dict('records')
        
        # 6. Enrich Layout
        results = []
        for res in top_results:
            # We already have data in CSV, but let's ensure structure matches frontend expectations
            
            # Dynamic re-enrichment (optional, but good for freshness if cache expired)
            # Since data_generator already did it, we primarily trust csv, 
            # but we can call api_manager if fields are missing.
            
            # Generate Itinerary
            itinerary = self._generate_itinerary(res, int(days))
            
            result_item = {
                "name": res['Place'],
                "score": round(res['score'], 2),
                "category": res['Category'],
                "budget": res['Budget'],
                "map": res.get('Map_Link', ''),
                "images": [res['Image']] if pd.notna(res['Image']) else [],
                "about": res.get('Description', ''),
                "Tags": res.get('Activities', ''), # Mapping Activities to Tags for frontend pill display
                "Price_Day": res.get('Price_Day', 3000),
                "Review": res.get('Review', 'A great place to visit!'),
                "Rating": res.get('Rating', 4.5),
                "Itinerary": itinerary,
                
                # Compatibility with legacy frontend fields just in case
                "Place": res['Place'],
                "Description": res.get('Description', ''),
                "Image": res.get('Image', '')
            }
            results.append(result_item)
            
        return results

    def get_all_states(self):
        return sorted(self.df['State'].unique().tolist())

    def get_destinations_by_state(self, state_name):
        results = self.df[self.df['State'].str.lower() == state_name.lower()].copy()
        top_results = results.to_dict('records')
        
        final_results = []
        for res in top_results:
             itinerary = self._generate_itinerary(res, 3)
             res['Itinerary'] = itinerary
             res['name'] = res['Place'] # map for frontend
             res['about'] = res.get('Description', '')
             if 'Image' in res and pd.notna(res['Image']):
                 res['images'] = [res['Image']]
             res['map'] = res.get('Map_Link', '')
             res['Tags'] = res.get('Activities', '')
             final_results.append(res)
             
        return final_results

    def get_place_details(self, place_name):
        """
        Retrieves full details for a specific place, including multiple images and hotels.
        """
        # Find place in dataframe
        place_data = self.df[self.df['Place'].str.lower() == place_name.lower()]
        
        if place_data.empty:
            return None
            
        res = place_data.iloc[0].to_dict()
        
        # Enrichment (Live) to get all images
        enriched = self.api_manager.enrich_place(res['Place'])
        
        # Merge enrichment
        res['images'] = enriched.get('images', []) if enriched else []
        if not res['images'] and pd.notna(res.get('Image')):
             res['images'] = [res['Image']]
        
        # Hotels: Fetch Real Data via OSM (Nominatim)
        real_hotels = self.api_manager.get_hotels(res['Place'])
        
        if real_hotels:
            # Sort by Rating (Desc) and Price (Asc)
            # Tuple sort: (-rating, price)
            real_hotels.sort(key=lambda x: (-x['rating'], x['price']))
            res['Hotels'] = real_hotels[:5] # Top 5
        else:
            # Fallback if OSM returns nothing (mock)
            budget = res.get('Budget', 'Medium')
            hotels_pool = {
                "Low": ["Zostel", "Local Guesthouse", "Backpacker Hostel", "City Lodge", "YMCA"],
                "Medium": ["Ginger Hotel", "Treebo Trend", "Standard Boutique Hotel", "Lemon Tree", "Ibis Styles"],
                "High": ["Taj Resorts", "The Oberoi", "Luxury Villa", "Marriott", "Hyatt Regency"]
            }
            names = random.sample(hotels_pool.get(budget, hotels_pool["Medium"]), 3)
            # Convert simple strings to dict structure for consistency
            res['Hotels'] = [{"name": n, "rating": 4.0, "price": 0, "address": "City Center"} for n in names]
        
        # Text fields
        res['about'] = enriched.get('about') if enriched else res.get('Description')
        res['map'] = enriched.get('map') if enriched else res.get('Map_Link')
        
        return res

    def _generate_itinerary(self, place_data, days):
        """
        Rule-based itinerary generation based on destination metadata.
        """
        itinerary = []
        name = place_data['Place']
        tags = place_data.get('Activities', '') + " " + place_data.get('Category', '')
        budget = place_data.get('Budget', 'Medium')
        
        hotels = {
            "Low": ["Zostel", "Local Guesthouse", "Backpacker Hostel"],
            "Medium": ["Ginger Hotel", "Treebo Trend", "Standard Boutique Hotel"],
            "High": ["Taj Resorts", "The Oberoi", "Luxury Villa"]
        }
        suggested_hotel = random.choice(hotels.get(budget, hotels["Medium"]))

        for day in range(1, days + 1):
            day_plan = {
                "Day": day,
                "Morning": f"Explore the scenic spots of {name}.",
                "Afternoon": f"Enjoy local {budget}-friendly cuisine.",
                "Evening": f"Relaxing evening walk.",
                "Night": f"Dinner at a local favorite.",
                "Hotel": suggested_hotel if day == 1 else "Same as Day 1",
            }
            
            if "Beach" in tags:
                if day == 1:
                    day_plan["Morning"] = "Sunrise by the ocean."
                    day_plan["Afternoon"] = "Water sports or beach volley."
                elif day == 2:
                     day_plan["Morning"] = "Visit nearby coastal villages."
            elif "Hill Station" in tags or "Mountain" in tags:
                if day == 1:
                    day_plan["Morning"] = "Trek to the highest viewpoint."
                    day_plan["Afternoon"] = "Visit tea/coffee plantations."
                
            itinerary.append(day_plan)
            
        return itinerary
