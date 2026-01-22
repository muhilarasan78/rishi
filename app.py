from flask import Flask, render_template, request, jsonify
from ml_engine import RecommendationEngine
import os

app = Flask(__name__)

# Initialize ML Engine
# Ensure data exists and is preprocessed
if not os.path.exists("tourism_data.csv"):
    import data_generator
    data_generator.generate_data()

if not os.path.exists("preprocessed_tourism_data.csv"):
    import preprocess
    preprocess.preprocess_data()

engine = RecommendationEngine()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    budget = data.get('budget', '')
    state = data.get('state', '')
    district = data.get('district', '')
    days = data.get('days', 3)
    interests = data.get('interests', '')
    
    recommendations = engine.get_recommendations(
        state=state, 
        district=district, 
        budget=budget, 
        interests=interests, 
        days=days
    )
    
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

