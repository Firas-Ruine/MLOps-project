from flask import Flask, request, jsonify
import joblib
import os

# Load the trained model
MODEL_PATH = 'src/models/text_sentiment_model.pkl'
model = joblib.load(MODEL_PATH)

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from request
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Make prediction
    prediction = model.predict([text])[0]  # Get the first prediction (as we have only one text input)

    # Return prediction as JSON
    return jsonify({"text": text, "sentiment": prediction})

if __name__ == '__main__':
    app.run(debug=True)
