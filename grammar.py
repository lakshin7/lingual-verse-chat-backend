from flask import Blueprint, request, jsonify
import logging
import os
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

grammar_bp = Blueprint('grammar', __name__)

# Initialize grammar correction
MODEL_TYPE = None
tool = None

try:
    import language_tool_python
    try:
        # Try with manual download first
        tool = language_tool_python.LanguageTool('en-US', remote_server='https://api.languagetool.org')
        MODEL_TYPE = "language_tool_remote"
        logger.info("Using remote LanguageTool server")
    except Exception as e:
        logger.warning(f"Remote server failed: {str(e)}. Trying local...")
        try:
            # Fallback to local with clean download
            cache_dir = os.path.expanduser('~/.cache/language_tool_python')
            if os.path.exists(cache_dir):
                import shutil
                shutil.rmtree(cache_dir)
            tool = language_tool_python.LanguageTool('en-US')
            MODEL_TYPE = "language_tool_local"
            logger.info("Using local LanguageTool")
        except Exception as e:
            logger.error(f"Local setup failed: {str(e)}")
except ImportError:
    logger.error("LanguageTool not installed!")

def correct_text(text: str) -> Tuple[str, str]:
    """Correct text using available model."""
    if not text or not isinstance(text, str):
        return text, "no_model"
    
    if MODEL_TYPE and tool:
        try:
            return tool.correct(text), MODEL_TYPE
        except Exception as e:
            logger.error(f"Correction failed: {str(e)}")
            return text, "error"
    return text, "no_model"

@grammar_bp.route('/correct', methods=['POST'])
def correct_grammar():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    user_input = request.json.get('message', "").strip()
    if not user_input:
        return jsonify({"error": "Field 'message' is required"}), 400

    corrected_text, model_used = correct_text(user_input)
    
    return jsonify({
        "original": user_input,
        "corrected": corrected_text,
        "model_used": model_used,
        "status": "success" if model_used not in ["no_model", "error"] else "warning"
    })