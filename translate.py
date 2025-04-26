from flask import Blueprint, request, jsonify
from deep_translator import GoogleTranslator

translate_bp = Blueprint('translate', __name__)

@translate_bp.route('/translate', methods=['POST'])
def translate():
    user_input = request.json.get('message')
    target_lang = request.json.get('target_lang', 'ta') 
    
    if not user_input:
        return jsonify({"error": "Field 'message' is required."}), 400
    
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(user_input)
        response = f"Translated: {translated}"
    except Exception as e:
        response = f"Translation Error: {e}"
    
    return jsonify({"reply": response})