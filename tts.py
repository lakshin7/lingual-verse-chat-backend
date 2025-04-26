from flask import Blueprint, request, jsonify
from gtts import gTTS
import os

tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/tts', methods=['POST'])
def tts():
    text = request.json.get('message')
    
    if not text:
        return jsonify({"error": "Field 'message' is required."}), 400
    
    try:
        tts = gTTS(text)
        audio_filename = "response.mp3"
        audio_path = os.path.join("static", audio_filename)
        tts.save(audio_path)
        
        audio_url = f"http://127.0.0.1:5001/static/{audio_filename}"
        response = "Audio response generated."
    except Exception as e:
        response = f"Text-to-Speech Error: {e}"
    
    return jsonify({"reply": response, "audio_url": audio_url})