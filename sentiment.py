from flask import Blueprint, request, jsonify
from textblob import TextBlob

sentiment_bp = Blueprint('sentiment', __name__)

@sentiment_bp.route('/sentiment', methods=['POST'])
def sentiment():
    user_input = request.json.get('message')
    
    if not user_input:
        return jsonify({"error": "Field 'message' is required."}), 400
    
    try:
        blob = TextBlob(user_input)
        sentiment = blob.sentiment.polarity
        
        if sentiment > 0:
            response = "Your message sounds positive!"
        elif sentiment < 0:
            response = "Your message sounds negative."
        else:
            response = "Your message sounds neutral."
    except Exception as e:
        response = f"Sentiment Analysis Error: {e}"
    
    return jsonify({"reply": response})