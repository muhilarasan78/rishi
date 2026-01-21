import pandas as pd
import random

def generate_data():
    regions = ["North India", "South India", "East India", "West India", "Central India", "International"]
    cats = ["Beach", "Adventure", "Nature", "Culture", "History", "City", "Relaxation"]
    
    # List of sample destinations
    destinations = [
        {"Place": "Goa", "Region": "West India", "Tags": "Beach, Party, Relaxation, Nightlife", "Budget": "Medium"},
        {"Place": "Manali", "Region": "North India", "Tags": "Adventure, Nature, Snow, Mountains", "Budget": "Low"},
        {"Place": "Kerala (Alleppey)", "Region": "South India", "Tags": "Nature, Backwaters, Relaxation, Boat", "Budget": "Medium"},
        {"Place": "Jaipur", "Region": "North India", "Tags": "Culture, History, Forts, City", "Budget": "Medium"},
        {"Place": "Leh Ladakh", "Region": "North India", "Tags": "Adventure, Mountains, Bike, Nature", "Budget": "High"},
        {"Place": "Andaman Islands", "Region": "South India", "Tags": "Beach, Scuba, Nature, Relaxation", "Budget": "High"},
        {"Place": "Rishikesh", "Region": "North India", "Tags": "Adventure, Spiritual, River, Nature", "Budget": "Low"},
        {"Place": "Varanasi", "Region": "North India", "Tags": "Spiritual, Culture, History, City", "Budget": "Low"},
        {"Place": "Munnar", "Region": "South India", "Tags": "Nature, Tea Gardens, Mountains, Relaxation", "Budget": "Medium"},
        {"Place": "Udaipur", "Region": "West India", "Tags": "Culture, Lakes, History, Romantic", "Budget": "High"},
        {"Place": "Darjeeling", "Region": "East India", "Tags": "Nature, Mountains, Tea, Culture", "Budget": "Medium"},
        {"Place": "Hampi", "Region": "South India", "Tags": "History, Ruins, Culture, Backpacking", "Budget": "Low"},
        {"Place": "Coorg", "Region": "South India", "Tags": "Nature, Coffee, Mountains, Relaxation", "Budget": "Medium"},
        {"Place": "Pondicherry", "Region": "South India", "Tags": "Beach, Culture, French, Relaxation", "Budget": "Medium"},
        {"Place": "Jaisalmer", "Region": "West India", "Tags": "Desert, Culture, History, Adventure", "Budget": "Medium"},
        {"Place": "Shimla", "Region": "North India", "Tags": "Mountains, Colonial, Nature, City", "Budget": "Medium"},
        {"Place": "Kolkata", "Region": "East India", "Tags": "City, Culture, History, Food", "Budget": "Low"},
        {"Place": "Mumbai", "Region": "West India", "Tags": "City, Nightlife, Beach, Bollywood", "Budget": "High"},
        {"Place": "Ooty", "Region": "South India", "Tags": "Mountains, Nature, Lake, Family", "Budget": "Medium"},
        {"Place": "Sikkim", "Region": "East India", "Tags": "Nature, Mountains, Monastery, Adventure", "Budget": "Medium"},
        {"Place": "Mysore", "Region": "South India", "Tags": "Culture, Palace, History, City", "Budget": "Low"},
        {"Place": "Agra", "Region": "North India", "Tags": "Taj Mahal, History, Culture, Landmark", "Budget": "Medium"},
        {"Place": "Gulmarg", "Region": "North India", "Tags": "Snow, Skiing, Mountains, Nature", "Budget": "High"},
        {"Place": "Rann of Kutch", "Region": "West India", "Tags": "Desert, Culture, Festival, Unique", "Budget": "Medium"},
        {"Place": "Khajuraho", "Region": "Central India", "Tags": "History, Temples, Culture, Art", "Budget": "Medium"},
        {"Place": "Ajanta Ellora", "Region": "West India", "Tags": "History, Caves, Ancient, Culture", "Budget": "Low"},
        {"Place": "Spiti Valley", "Region": "North India", "Tags": "Adventure, Remote, Mountains, Nature", "Budget": "High"},
        {"Place": "Wayanad", "Region": "South India", "Tags": "Nature, Wildlife, Mountains, Greenery", "Budget": "Low"},
        {"Place": "Cherrapunji", "Region": "East India", "Tags": "Nature, Rain, Waterfalls, Greenery", "Budget": "Medium"},
        {"Place": "Mount Abu", "Region": "West India", "Tags": "Hill Station, Temples, Nature, Lake", "Budget": "Low"},
    ]
    
    # Expand dataset or add descriptions
    data = []
    for d in destinations:
        # Generate a dummy description
        desc = f"Experience the amazing {d['Tags']} at {d['Place']}. Perfect for a {d['Budget']} budget trip."
        d['Description'] = desc
        # Add basic prices
        if d['Budget'] == "Low":
            d['Price_Day'] = 2000
        elif d['Budget'] == "Medium":
            d['Price_Day'] = 5000
        else:
            d['Price_Day'] = 10000
        
        data.append(d)

    df = pd.DataFrame(data)
    df.to_csv("tourism_data.csv", index=False)
    print("tourism_data.csv generated with", len(df), "records.")

if __name__ == "__main__":
    generate_data()
