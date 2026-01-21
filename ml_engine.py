import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import random
import os

class RecommendationEngine:
    """
    1. Implement RecommendationEngine class
    Handles data loading, ML-based ranking, and itinerary generation.
    """
    def __init__(self, data_path="preprocessed_tourism_data.csv"):
        # Ensure preprocessed data exists
        if not os.path.exists(data_path):
            import preprocess
            preprocess.preprocess_data()
            
        self.df = pd.read_csv(data_path)
        self._initialize_ml()

    def _initialize_ml(self):
        """
        2. Implement TF-IDF vectorization and Cosine Similarity logic
        Prepares the vectorizer and fits it on the preprocessed content.
        """
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['Content'])

    def get_recommendations(self, region, budget, interests, days=3):
        # Start with full dataset
        recommendations = self.df.copy()
        
        # Soft filter by Region
        if region:
            region_matches = recommendations[recommendations['Region'].str.contains(region, case=False, na=False)]
            if not region_matches.empty:
                recommendations = region_matches

        # Compute Similarity (ML Logic)
        user_profile = interests if interests else "travel"
        user_tfidf = self.tfidf.transform([user_profile.lower()])
        cosine_sim = linear_kernel(user_tfidf, self.tfidf_matrix)
        
        # Rank by ML scores
        self.df['similarity'] = cosine_sim[0]
        results = recommendations.merge(self.df[['Place', 'similarity']], on='Place', suffixes=('', '_new'))
        
        # Strict Budget filtering
        if budget:
            results = results[results['Budget'].str.lower() == budget.lower()]
            
        results = results.sort_values(by='similarity', ascending=False)
        top_results = results.head(5).to_dict('records')
        
        # 3. Implement itinerary generation logic (rules + ML results)
        for res in top_results:
            res['Itinerary'] = self._generate_itinerary(res, int(days))
            
        return top_results

    def _generate_itinerary(self, place_data, days):
        """
        Rule-based itinerary generation based on destination metadata (Tags/Budget).
        """
        itinerary = []
        name = place_data['Place']
        tags = place_data.get('Tags', '')
        budget = place_data.get('Budget', 'Medium')
        
        # Stay rules (based on budget)
        hotels = {
            "Low": ["Zostel", "Local Guesthouse", "Backpacker Hostel"],
            "Medium": ["Ginger Hotel", "Treebo Trend", "Standard Boutique Hotel"],
            "High": ["Taj Resorts", "The Oberoi", "Luxury Villa"]
        }
        suggested_hotel = random.choice(hotels.get(budget, hotels["Medium"]))

        # Activity rules (based on tags)
        for day in range(1, days + 1):
            day_plan = {
                "Day": day,
                "Morning": f"Explore the scenic spots of {name}.",
                "Afternoon": f"Enjoy local {budget}-friendly cuisine and relax.",
                "Evening": f"Visit local markets or cultural centers.",
                "Night": f"Dinner at a highly-rated restaurant.",
                "Hotel": suggested_hotel if day == 1 else "Same as Day 1",
                "EstimatedCost": place_data.get("Price_Day", 3000)
            }
            
            if "Beach" in tags:
                if day == 1:
                    day_plan["Morning"] = "Visit the main beach for sunrise and morning walk."
                    day_plan["Afternoon"] = "Relax at a beach shack with coconut water."
                else:
                    day_plan["Morning"] = "Water sports activities (Jet Ski, Parasailing)."
                    day_plan["Afternoon"] = "Explore hidden coves and quieter beaches."
            elif any(t in tags for t in ["Mountain", "Adventure", "Nature"]):
                if day == 1:
                    day_plan["Morning"] = "Short trek to a panoramic viewpoint."
                    day_plan["Afternoon"] = "Visit a local monastery or temple."
                else:
                    day_plan["Morning"] = "Full day excursion to higher altitudes."
                    day_plan["Afternoon"] = "Adventure activities like paragliding or rock climbing."
                
            itinerary.append(day_plan)
            
        return itinerary
