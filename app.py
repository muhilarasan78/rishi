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

@app.route('/states')
def states_directory():
    all_states = engine.get_all_states()
    return render_template('states.html', states=all_states)

@app.route('/state/<state_name>')
def state_detail(state_name):
    destinations = engine.get_destinations_by_state(state_name)
    return render_template('state_detail.html', state_name=state_name, destinations=destinations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

