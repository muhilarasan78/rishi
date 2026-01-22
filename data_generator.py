import pandas as pd
import random

def generate_data():
    # Comprehensive destination list covering 28 states with non-temple focus
    # Format: {Place, State, District, Tags, Budget}
    destinations = [
        # Tamil Nadu
        {"Place": "Ooty", "State": "Tamil Nadu", "District": "Nilgiris", "Tags": "Hill Station, Nature, Mountains, Tea Gardens", "Budget": "Medium"},
        {"Place": "Kodaikanal", "State": "Tamil Nadu", "District": "Dindigul", "Tags": "Hill Station, Lake, Nature, Relaxation", "Budget": "Medium"},
        {"Place": "Mahabalipuram", "State": "Tamil Nadu", "District": "Chengalpattu", "Tags": "Heritage, Beach, History, Architecture", "Budget": "Low"},
        {"Place": "Yercaud", "State": "Tamil Nadu", "District": "Salem", "Tags": "Hill Station, Nature, Budget Friendly", "Budget": "Low"},
        {"Place": "Marina Beach", "State": "Tamil Nadu", "District": "Chennai", "Tags": "Beach, City, Landmark, Evening Walk", "Budget": "Low"},
        
        # Kerala
        {"Place": "Munnar", "State": "Kerala", "District": "Idukki", "Tags": "Nature, Tea Gardens, Mountains, Honeymoon", "Budget": "Medium"},
        {"Place": "Alleppey Backwaters", "State": "Kerala", "District": "Alappuzha", "Tags": "Nature, Backwaters, Houseboat, Relaxation", "Budget": "High"},
        {"Place": "Wayanad", "State": "Kerala", "District": "Wayanad", "Tags": "Nature, Wildlife, Waterfall, Trekking", "Budget": "Medium"},
        {"Place": "Varkala Beach", "State": "Kerala", "District": "Thiruvananthapuram", "State": "Kerala", "State": "Kerala", "District": "Thiruvananthapuram", "Tags": "Beach, Cliff, Relaxation, Adventure", "Budget": "Medium"},
        {"Place": "Athirappilly Falls", "State": "Kerala", "District": "Thrissur", "Tags": "Nature, Waterfall, Photography, Forest", "Budget": "Low"},

        # Karnataka
        {"Place": "Coorg", "State": "Karnataka", "District": "Kodagu", "Tags": "Nature, Coffee Estates, Mountains, Relax", "Budget": "Medium"},
        {"Place": "Hampi", "State": "Karnataka", "District": "Vijayanagara", "Tags": "Heritage, History, Ruins, Culture", "Budget": "Low"},
        {"Place": "Gokarna", "State": "Karnataka", "District": "Uttara Kannada", "Tags": "Beach, Relax, Hippie, Nature", "Budget": "Low"},
        {"Place": "Chikkamagaluru", "State": "Karnataka", "District": "Chikkamagaluru", "Tags": "Nature, Coffee, Mountains, Trekking", "Budget": "Medium"},
        {"Place": "Bandipur", "State": "Karnataka", "District": "Chamarajanagar", "Tags": "Wildlife, Safari, Nature, Adventure", "Budget": "High"},

        # Andhra Pradesh
        {"Place": "Araku Valley", "State": "Andhra Pradesh", "District": "Visakhapatnam", "Tags": "Nature, Hills, Coffee, Tribes", "Budget": "Low"},
        {"Place": "Gandikota", "State": "Andhra Pradesh", "District": "Kadapa", "Tags": "Nature, Adventure, Grand Canyon, History", "Budget": "Low"},
        {"Place": "Vizag Beaches", "State": "Andhra Pradesh", "District": "Visakhapatnam", "Tags": "Beach, City, Port, Nature", "Budget": "Medium"},

        # Telangana
        {"Place": "Hyderabad", "State": "Telangana", "District": "Hyderabad", "Tags": "City, Culture, History, Food", "Budget": "Medium"},
        {"Place": "Ananthagiri Hills", "State": "Telangana", "District": "Vikarabad", "Tags": "Hill Station, Nature, Trekking", "Budget": "Low"},

        # Himachal Pradesh
        {"Place": "Shimla", "State": "Himachal Pradesh", "District": "Shimla", "Tags": "Hill Station, Snow, Mountains, Colonial", "Budget": "Medium"},
        {"Place": "Manali", "State": "Himachal Pradesh", "District": "Kullu", "Tags": "Hill Station, Adventure, Snow, Honeymoon", "Budget": "Medium"},
        {"Place": "Dharamshala", "State": "Himachal Pradesh", "District": "Kangra", "Tags": "Hill Station, Culture, Mountains, Dalai Lama", "Budget": "Low"},

        # Uttarakhand
        {"Place": "Nainital", "State": "Uttarakhand", "District": "Nainital", "Tags": "Hill Station, Lake, Nature, Family", "Budget": "Medium"},
        {"Place": "Rishikesh", "State": "Uttarakhand", "District": "Dehradun", "Tags": "Adventure, River, Nature, Spiritual", "Budget": "Low"},

        # Rajasthan
        {"Place": "Jaipur", "State": "Rajasthan", "District": "Jaipur", "Tags": "City, History, Forts, Culture", "Budget": "Medium"},
        {"Place": "Udaipur", "State": "Rajasthan", "District": "Udaipur", "Tags": "City, Lake, History, Romantic", "Budget": "High"},
        {"Place": "Jaisalmer", "State": "Rajasthan", "District": "Jaisalmer", "Tags": "Desert, Safari, History, Culture", "Budget": "Medium"},

        # Goa
        {"Place": "Calangute", "State": "Goa", "District": "North Goa", "Tags": "Beach, Party, Nightlife, Shopping", "Budget": "Medium"},
        {"Place": "Palolem", "State": "Goa", "District": "South Goa", "Tags": "Beach, Quiet, Relax, Nature", "Budget": "Medium"},

        # Maharashtra
        {"Place": "Lonavala", "State": "Maharashtra", "District": "Pune", "Tags": "Hill Station, Nature, Monsoon, Weekend", "Budget": "Low"},
        {"Place": "Mumbai (Colaba)", "State": "Maharashtra", "District": "Mumbai City", "Tags": "City, Sea, History, Shopping", "Budget": "High"},

        # West Bengal
        {"Place": "Darjeeling", "State": "West Bengal", "District": "Darjeeling", "Tags": "Hill Station, Tea, Mountains, Toy Train", "Budget": "Medium"},

        # Sikkim
        {"Place": "Gangtok", "State": "Sikkim", "District": "East Sikkim", "Tags": "Hill Station, Nature, Mountains, Monastery", "Budget": "Medium"},

        # Jammu & Kashmir
        {"Place": "Gulmarg", "State": "Jammu & Kashmir", "District": "Baramulla", "Tags": "Snow, Skiing, Mountains, Nature", "Budget": "High"},
        {"Place": "Srinagar", "State": "Jammu & Kashmir", "District": "Srinagar", "Tags": "Nature, Lake, Houseboat, Mountains", "Budget": "High"},
        
        # Adding more placeholder for other states to ensure 28 coverage
        {"Place": "Tawang", "State": "Arunachal Pradesh", "District": "Tawang", "Tags": "Mountains, Nature, Monastery, High Altitude", "Budget": "High"},
        {"Place": "Kaziranga", "State": "Assam", "District": "Golaghat", "Tags": "Wildlife, Safari, Rhino, Nature", "Budget": "Medium"},
        {"Place": "Bodh Gaya", "State": "Bihar", "State": "Bihar", "District": "Gaya", "Tags": "History, Culture, Spiritual, Landmark", "Budget": "Low"},
        {"Place": "Bastar", "State": "Chhattisgarh", "District": "Bastar", "Tags": "Nature, Waterfalls, Tribes, Culture", "Budget": "Low"},
        {"Place": "Rann of Kutch", "State": "Gujarat", "District": "Kutch", "Tags": "Desert, Culture, Festival, Unique", "Budget": "Medium"},
        {"Place": "Kurukshetra", "State": "Haryana", "District": "Kurukshetra", "Tags": "History, Landmark, Museum", "Budget": "Low"},
        {"Place": "Netarhat", "State": "Jharkhand", "District": "Latehar", "Tags": "Nature, Hill Station, Sunset", "Budget": "Low"},
        {"Place": "Khajuraho", "State": "Madhya Pradesh", "District": "Chhatarpur", "Tags": "History, Architecture, Heritage", "Budget": "Medium"},
        {"Place": "Imphal", "State": "Manipur", "District": "Imphal West", "Tags": "City, Culture, Lake, Nature", "Budget": "Low"},
        {"Place": "Shillong", "State": "Meghalaya", "District": "East Khasi Hills", "Tags": "Hill Station, Nature, Waterfalls, Music", "Budget": "Medium"},
        {"Place": "Aizawl", "State": "Mizoram", "District": "Aizawl", "Tags": "Hill Station, Nature, Culture", "Budget": "Low"},
        {"Place": "Kohima", "State": "Nagaland", "District": "Kohima", "Tags": "Hill Station, Culture, History, War Cemetery", "Budget": "Low"},
        {"Place": "Puri Beach", "State": "Odisha", "District": "Puri", "Tags": "Beach, Nature, Relaxation", "Budget": "Low"},
        {"Place": "Amritsar", "State": "Punjab", "District": "Amritsar", "Tags": "City, Culture, History, Food", "Budget": "Low"},
        {"Place": "Agartala", "State": "Tripura", "District": "West Tripura", "Tags": "City, Palace, Culture, History", "Budget": "Low"},
        {"Place": "Agra", "State": "Uttar Pradesh", "District": "Agra", "Tags": "History, Taj Mahal, Seventh Wonder, City", "Budget": "Medium"},
    ]
    
    # Process and add descriptions/prices
    data = []
    for d in destinations:
        # Region logic (simplified mapping)
        north_states = ["Himachal Pradesh", "Uttarakhand", "Jammu & Kashmir", "Punjab", "Haryana", "Uttar Pradesh", "Rajasthan"]
        south_states = ["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh", "Telangana", "Goa"]
        east_states = ["West Bengal", "Sikkim", "Arunachal Pradesh", "Assam", "Meghalaya", "Mizoram", "Nagaland", "Tripura", "Bihar", "Jharkhand", "Odisha"]
        
        if d['State'] in north_states: d['Region'] = "North India"
        elif d['State'] in south_states: d['Region'] = "South India"
        elif d['State'] in east_states: d['Region'] = "East India"
        else: d['Region'] = "Central India"

        desc = f"Discover the beauty of {d['Place']} in {d['District']}, {d['State']}. A perfect spot for {d['Tags']}."
        d['Description'] = desc
        
        if d['Budget'] == "Low": d['Price_Day'] = 2000
        elif d['Budget'] == "Medium": d['Price_Day'] = 5000
        else: d['Price_Day'] = 10000
        
        data.append(d)

    df = pd.DataFrame(data)
    df.to_csv("tourism_data.csv", index=False)
    print(f"tourism_data.csv generated with {len(df)} records covering multiple states.")

if __name__ == "__main__":
    generate_data()
