import pandas as pd
import scipy.sparse as sparse
import implicit
from implicit.als import AlternatingLeastSquares
import joblib

# Load your dataset and ensure 'Prices' is a numeric type
try:
    data = pd.read_csv('Event.csv')  # Update with the correct path to your CSV file
except FileNotFoundError:
    print("Error: The dataset file was not found.")
    exit()
except pd.errors.EmptyDataError:
    print("Error: The dataset file is empty.")
    exit()

data['Prices'] = pd.to_numeric(data['Prices'], errors='coerce')  # Convert to numeric, set errors to NaN
data.dropna(subset=['Prices'], inplace=True)  # Drop rows where 'Prices' couldn't be converted

# Function to filter data based on user input
def filter_data(data, location, max_price, theme):
    filtered_data = data[
        (data['Location'] == location) & 
        (data['Theme'] == theme)
    ]

    if filtered_data.empty:
        print("No data available for the given location and theme.")
        return filtered_data

    if max_price < filtered_data['Prices'].min():
        print("No data available for the given budget.")
        return pd.DataFrame()

    filtered_data = filtered_data[filtered_data['Prices'] <= max_price]
    
    return filtered_data

# Function to train the model using implicit ALS
def train_model(location, max_price, theme):
    filtered_data = filter_data(data, location, max_price, theme)

    if filtered_data.empty:
        return None, None

    # Create user-item matrix (for collaborative filtering)
    user_item_matrix = sparse.csr_matrix(
        (filtered_data['Ratings'], (filtered_data['User ID'], filtered_data['Vendor Choosen']))
    )

    # Initialize the ALS model from the implicit library
    model = AlternatingLeastSquares(factors=50, iterations=10)
    model.fit(user_item_matrix.T)  # Transpose is needed

    # Save the trained model
    joblib.dump(model, f'implicit_collaborative_filtering_model_{location}_{max_price}_{theme}.pkl')
    print(f"Model saved as 'implicit_collaborative_filtering_model_{location}_{max_price}_{theme}.pkl'")

    return model, filtered_data

# Function to recommend venues based on user input
def recommend_venues(model, filtered_data, top_n=5):
    recommendations = []

    user_item_matrix = sparse.csr_matrix(
        (filtered_data['Ratings'], (filtered_data['User ID'], filtered_data['Vendor Choosen']))
    )

    # Get recommendations for a dummy user (user ID 0)
    user_id = 0
    recommended = model.recommend(user_id, user_item_matrix, N=top_n)

    for vendor_id, score in recommended:
        # Extract relevant venue information from filtered data
        venue_info = filtered_data[filtered_data['Vendor Choosen'] == vendor_id].iloc[0]
        venue_name = venue_info['Venue Choosen']
        price = venue_info['Prices']
        recommendations.append((venue_name, vendor_id, price, score))

    return recommendations

# Example usage
if __name__ == "__main__":
    location = input("Enter the location: ")
    max_price = float(input("Enter the maximum price: "))
    theme = input("Enter the theme: ")

    model, filtered_data = train_model(location, max_price, theme)

    if model:
        print("Model trained successfully!!")
        recommendations = recommend_venues(model, filtered_data)
        if recommendations:
            print("Recommended Venues:")
            for venue_name, vendor_id, price, score in recommendations:
                print(f"Venue: {venue_name}, Vendor: {vendor_id}, Price: {price}, Score: {score:.2f}")
        else:
            print("No venues found within the specified budget and criteria.")
    else:
        print("Model training failed.")
