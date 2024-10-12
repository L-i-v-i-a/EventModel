import pandas as pd
import joblib  # Make sure to import joblib for saving the model

import pandas as pd

# Sample data for the dataset
data = {
    'Vendor Choosen': ['Venue A', 'Venue B', 'Venue C', 'Venue D', 'Venue E','Venue F'],
    'Location': ['Abuja', 'Lagos', 'Abuja', 'Port Harcourt', 'Lagos','Abuja'],
    'Prices': [300000, 500000, 450000, 600000, 350000, 20000],
    'Theme': ['Wedding', 'Corporate', 'Wedding', 'Birthday', 'Wedding', 'Wedding'],
    'Services': [
        'Catering, Decoration, Sound System',
        'Catering, Audio-Visual, Decoration',
        'Catering, Decoration, Lighting',
        'Catering, Decoration, Music',
        'Catering, Decoration, Photography',
        'Catering, Decoration, Lighting'
    ],
    'Ratings': [4.5, 4.0, 4.7, 4.3, 4.6,4.5]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the dataset to a CSV file
df.to_csv("Event2.csv", index=False)

print("Dataset created and saved as 'Event.csv':")
print(df)


# Load the dataset
data = pd.read_csv("Event2.csv")

# Function to filter venues based on user input
def filter_venues(data, location, theme, max_price):
    filtered_data = data[
        (data['Location'] == location) & 
        (data['Theme'] == theme) & 
        (data['Prices'] <= max_price)
    ]
    
    if filtered_data.empty:
        print("No venues found for the given criteria.")
        return pd.DataFrame()  # Return empty DataFrame

    return filtered_data[['Vendor Choosen', 'Prices', 'Theme', 'Services', 'Ratings', 'Location']]

# Main function to get recommendations
def get_recommendations(location, theme, max_price):
    recommendations = filter_venues(data, location, theme, max_price)
    return recommendations

# Enhanced input handling
def get_user_input():
    while True:
        location = input("Enter the location: ")
        theme = input("Enter the theme: ")
        try:
            max_price = float(input("Enter the maximum price: "))
            if max_price < 0:
                raise ValueError("Price must be a non-negative number.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
    return location, theme, max_price

# Function to save the recommendations to a file
def save_recommendations(recommendations, location, max_price, theme):
    filename = f'recommendations_{location}_{max_price}_{theme}.csv'
    recommendations.to_csv(filename, index=False)  # Save recommendations to a CSV file
    print(f"Recommendations saved as '{filename}'.")

if __name__ == "__main__":
    location, theme, max_price = get_user_input()
    recommendations = get_recommendations(location, theme, max_price)

    if not recommendations.empty:
        print("Recommended Venues:")
        for index, row in recommendations.iterrows():
            print(f"Venue: {row['Vendor Choosen']}, Price: {row['Prices']}, Theme: {row['Theme']}, Services: {row['Services']}, Ratings: {row['Ratings']}, Location: {row['Location']}")
        
        save_recommendations(recommendations, location, max_price, theme)  # Save recommendations to a file
    else:
        print("No recommendations found.")
