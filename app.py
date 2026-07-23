from flask import Flask, render_template, request
import pandas as pd
import joblib

# Create Flask App
app = Flask(__name__)

# Load trained model
model = joblib.load("house_price_model.pkl")

# Load feature columns
feature_columns = joblib.load("feature_columns.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    # Get user input
    area = float(request.form["area"])
    bedrooms = int(request.form["bedrooms"])
    bathrooms = int(request.form["bathrooms"])
    floors = int(request.form["floors"])
    year = int(request.form["year"])

    location = request.form["location"]
    condition = request.form["condition"]
    garage = request.form["garage"]

    # Convert input into DataFrame
    sample_house = pd.DataFrame({
        "Area": [area],
        "Bedrooms": [bedrooms],
        "Bathrooms": [bathrooms],
        "Floors": [floors],
        "YearBuilt": [year],

        "Location_Suburban": [1 if location == "Suburban" else 0],
        "Location_Urban": [1 if location == "Urban" else 0],

        "Condition_Excellent": [1 if condition == "Excellent" else 0],
        "Condition_Good": [1 if condition == "Good" else 0],

        "Garage_Yes": [1 if garage == "Yes" else 0]
    })

    # Arrange columns in the same order as training
    sample_house = sample_house.reindex(columns=feature_columns, fill_value=0)

    # Predict
    predicted_price = model.predict(sample_house)[0]

    return render_template(
        "index.html",
        prediction=f"₹ {predicted_price:,.2f}"
    )

if __name__ == "__main__":
    app.run(debug=True)