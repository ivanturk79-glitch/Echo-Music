import os
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
MUSIC_DIR = os.path.abspath('/sdcard/музыка')
COVERS_DIR = os.path.join(MUSIC_DIR, 'covers')
ALLOWED_EXTENSIONS = {'.mp3', '.flac', '.wav', '.ogg', '.m4a'}

@app.route('/')
def index():
    return send_from_directory(MUSIC_DIR, 'index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    files = [f for f in os.listdir(MUSIC_DIR)
             if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]
    if query:
        files = [f for f in files if query in f.lower()]
    return jsonify([{'name': f, 'artist': 'Local Track'} for f in files])

@app.route('/covers/<path:filename>')
def cover(filename):
    return send_from_directory(COVERS_DIR, filename)

@app.route('/stream/<path:filename>')
def stream(filename):
    return send_from_directory(MUSIC_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
