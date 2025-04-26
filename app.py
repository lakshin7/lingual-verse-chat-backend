from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os

from grammar import grammar_bp
from translate import translate_bp
from tts import tts_bp
from sentiment import sentiment_bp
from multilingual import multilingual_bp
from speech import speech_bp

app = Flask(__name__)
CORS(app) 

app.register_blueprint(grammar_bp)
app.register_blueprint(translate_bp)
app.register_blueprint(tts_bp)
app.register_blueprint(sentiment_bp)
app.register_blueprint(multilingual_bp)
app.register_blueprint(speech_bp)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True)
