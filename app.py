from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the model
model = joblib.load('collaborative_filtering_model.pkl')

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    # Extract data from the request
    data = request.json
    location = data.get('location')
    max_price = data.get('max_price')
    theme = data.get('theme')
    
    # Perform recommendations logic here (e.g., filtering, prediction)
    # This assumes you've integrated filtering and prediction logic from earlier
    # filtered_data = some_filter_function(location, max_price, theme)
    
    # Return a mock response for now (replace with actual model prediction logic)
    recommendations = [
        {"venue": "Lawood Event Center", "vendor": "Esther", "price": 150000, "rating": 2},
        {"venue": "JJJISA Event Center", "vendor": "Tonia", "price": 400000, "rating": 5}
    ]
    
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
