from flask import Blueprint, request, jsonify
import io
import logging
import numpy as np

try:
    import soundfile as sf
    AUDIO_SUPPORT = True
except ImportError:
    AUDIO_SUPPORT = False
    logging.warning("soundfile not installed - audio features disabled")

speech_bp = Blueprint('speech', __name__)

@speech_bp.route('/analyze', methods=['POST'])
def analyze_audio():
    if not AUDIO_SUPPORT:
        return jsonify({"error": "Audio processing not available"}), 501
        
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    
    try:
        # Read audio from memory
        audio_data, samplerate = sf.read(io.BytesIO(file.read()))
        
        return jsonify({
            "duration": len(audio_data)/samplerate,
            "sample_rate": samplerate,
            "channels": 1 if len(audio_data.shape) == 1 else audio_data.shape[1],
            "samples": len(audio_data)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@speech_bp.route('/check_audio_support')
def check_support():
    return jsonify({
        "audio_supported": AUDIO_SUPPORT,
        "message": "soundfile available" if AUDIO_SUPPORT else "Install soundfile for audio features"
    })