from flask import Blueprint, request, jsonify
from deep_translator import GoogleTranslator


multilingual_bp = Blueprint('multilingual', __name__)

@multilingual_bp.route('/multilingual', methods=['POST'])
def multilingual():
    user_input = request.json.get('message')
    source_lang = request.json.get('source_lang', 'auto')  
    target_lang = request.json.get('target_lang', 'en')    
    
    if not user_input:
        return jsonify({"error": "Field 'message' is required."}), 400
    
    
    translated = GoogleTranslator(source=source_lang, target=target_lang).translate(user_input)
    response = f"Translated: {translated}"
    
    return jsonify({"reply": response})