from flask import Flask, render_template, request, jsonify, send_file
import os
from models.text_to_image import generate_image_from_text
from models.image_to_text import extract_text_from_image
from models.text_to_video import create_video_from_text
from models.text_to_audio import create_audio_from_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'assets/uploads'
app.config['ASSETS'] = {
    'images': 'assets/images',
    'videos': 'assets/videos',
    'audio': 'assets/audio'
}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ASSETS']['images'], exist_ok=True)
os.makedirs(app.config['ASSETS']['videos'], exist_ok=True)
os.makedirs(app.config['ASSETS']['audio'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

# Text-to-Image (Stable Diffusion)
@app.route('/generate-image', methods=['POST'])
def generate_image():
    text = request.json.get('text')
    image_path = generate_image_from_text(text, app.config['ASSETS']['images'])
    return jsonify({'image_url': image_path})

# Image-to-Text (PyTesseract)
@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    image = request.files['image']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)
    text = extract_text_from_image(image_path)
    return jsonify({'text': text})

# Text-to-Video (Placeholder)
@app.route('/generate-video', methods=['POST'])
def generate_video():
    text = request.json.get('text')
    video_path = create_video_from_text(text, app.config['ASSETS']['videos'])
    return send_file(video_path, as_attachment=True)

# Text-to-Audio (gTTS)
@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    text = request.json.get('text')
    audio_path = create_audio_from_text(text, app.config['ASSETS']['audio'])
    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
