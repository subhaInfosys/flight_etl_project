import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the trained model once at startup
model = joblib.load("flight_delay_model.pkl")
model_features = model.feature_names_in_

@app.route('/')
def home():
    return "✈️ Flight Delay Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON input
        input_data = request.json
        input_df = pd.get_dummies(pd.DataFrame([input_data]))

        # Align input with model features
        input_df = input_df.reindex(columns=model_features, fill_value=0)

        # Make prediction
        prediction = model.predict(input_df)[0]
        result = "delayed" if prediction == 1 else "on time"
        
        return jsonify({
            "prediction": result,
            "input": input_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
