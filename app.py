# app.py flask app
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from recommendations import main as get_movie_recommendations
from face_detection import detect_and_save_face

app = Flask(__name__, static_url_path='', static_folder='Website')
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def serve_index():
    return send_from_directory('Website', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    if detect_and_save_face(image_path):
        recommendations = get_movie_recommendations()
        return jsonify({'message': 'Image uploaded successfully', 'filename': filename, 'recommendations': recommendations})
    else:
        return jsonify({'error': 'No face detected in the image'}), 400

if __name__ == '__main__':
    app.run(debug=True)
