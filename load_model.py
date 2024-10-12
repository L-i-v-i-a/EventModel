import joblib

# Load the model using joblib
model = joblib.load('collaborative_filtering_model.pkl')

# Now you can use the loaded model
print("Model loaded successfully:", model)
