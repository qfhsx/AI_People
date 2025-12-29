import os
from flask import Flask, jsonify
from flask_cors import CORS
from .api.routes import api_bp

# Define temp dir path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

# Check if temp dir exists
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

app = Flask(__name__, static_folder=TEMP_DIR, static_url_path='/static/temp')
CORS(app)  # Enable CORS for frontend

app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/health')
def health():
    return jsonify({"status": "ok"})
