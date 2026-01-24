import pandas as pd
import time
import os
import random
# Replaced GooglePlacesHelper with TripGenixAPIManager
from api_manager import TripGenixAPIManager

def generate_reviews(place_name, category):
    """
    Generates a realistic review based on the place name and category.
    """
    templates = {
        "Hill Station": [
            f"The views at {place_name} are absolutely breathtaking! The misty mountains were a dream.",
            f"Had a wonderful time at {place_name}. Perfect weather and great trek routes.",
            f"{place_name} is a paradise for nature lovers. Don't miss the sunrise points!"
        ],
        "Beach": [
            f"{place_name} has some of the cleanest waters I've seen. Great for a relaxing swim.",
            f"Loved the vibe at {place_name}! The sunsets were magical and the seafood was amazing.",
            f"A perfect beach getaway. {place_name} was vibrant yet peaceful in the mornings."
        ],
        "Heritage": [
            f"The architecture at {place_name} is stunning. A walk through history.",
            f"{place_name} is a must-visit for history buffs. The guide explained everything so well.",
            f"Incredible craftsmanship! {place_name} left us awestruck."
        ],
        "Adventure": [
            f"The adrenaline rush at {place_name} was insane! Highly recommend the adventure sports.",
            f"If you love thrills, {place_name} is the place to be. Unforgettable experience.",
            f"Great camping spots and thrilling activities at {place_name}."
        ],
        "Spiritual": [
            f"Felt so peaceful at {place_name}. A truly spiritual experience.",
            f"The energy at {place_name} is divine. A great place to meditate and reflect.",
            f"Beautiful temple architecture and serene atmosphere at {place_name}."
        ],
        "Wildlife": [
            f"Saw so many animals at {place_name}! The safari was well organized.",
            f"{place_name} is a haven for wildlife photographers. Spotted a rare species!",
            f"A lush green sanctuary. {place_name} is teeming with life."
        ],
        "Backwaters": [
            f"The houseboats at {place_name} are a unique experience. So calm and relaxing.",
            f"Cruising through the backwaters of {place_name} was the highlight of our trip.",
            f"Serene and beautiful. {place_name} is the Venice of the East."
        ]
    }
    
    # Default fallbacks
    generic = [
        f"{place_name} exceeded our expectations. Will definitely visit again!",
        f"A lovely destination. {place_name} has so much to offer.",
        f"Great food, great people, and amazing sights at {place_name}."
    ]
    
    # Pick a template based on category or generic
    choices = templates.get(category, generic) + generic
    return random.choice(choices)

def generate_data():
    api_manager = TripGenixAPIManager()
    data = []
    
    # Check if external dataset exists
    if os.path.exists("external_dataset.csv"):
        print("Loading destinations from external_dataset.csv...")
        try:
            raw_df = pd.read_csv("external_dataset.csv")
            destinations = raw_df.to_dict('records')
        except Exception as e:
            print(f"Error reading external dataset: {e}")
            destinations = []
    else:
        print("external_dataset.csv not found. Using fallback list.")
        # Fallback list (truncated for brevity since we expect the CSV)
        destinations = [
            {"Place": "Ooty", "State": "Tamil Nadu", "District": "Nilgiris", "Category": "Hill Station", "Activities": "Boating", "Budget": "Medium", "Duration_Suitability": "3 days"}
        ]

    print(f"Starting data enrichment process for {len(destinations)} destinations...")
    
    for i, d in enumerate(destinations):
        print(f"Processing {i+1}/{len(destinations)}: {d['Place']}...")
        
        # 1. Fetch Dynamic Data
        enriched = api_manager.enrich_place(d['Place'])
        
        # 2. Merge Data
        if enriched:
            d['Description'] = enriched['about']
            d['Image'] = enriched['images'][0] if enriched['images'] else "https://via.placeholder.com/800x500"
            d['Map_Link'] = enriched['map']
            d['Latitude'] = enriched['location']['lat']
            d['Longitude'] = enriched['location']['lon']
        else:
            d['Description'] = f"Explore {d['Place']}."
            d['Image'] = "https://via.placeholder.com/800x500"
            d['Map_Link'] = ""
            d['Latitude'] = 0.0
            d['Longitude'] = 0.0

        # Review Generation
        d['Review'] = generate_reviews(d['Place'], d['Category'])
        d['Rating'] = random.choice([4.2, 4.5, 4.7, 4.8, 4.9, 5.0]) 

        # 3. Create Combined Features for TF-IDF
        d['Combined_Features'] = f"{d['Category']} {d['Activities']} {d['Budget']} {d['State']} {d['Description']} {d['Review']}"

        # 4. Standard Price
        if d['Budget'] == "Low": d['Price_Day'] = 2500
        elif d['Budget'] == "Medium": d['Price_Day'] = 5500
        else: d['Price_Day'] = 12000

        data.append(d)
        time.sleep(0.1) # Be nice to APIs

    df = pd.DataFrame(data)
    df.to_csv("tourism_data.csv", index=False)
    print(f"tourism_data.csv generated with {len(df)} records.")

if __name__ == "__main__":
    generate_data()
