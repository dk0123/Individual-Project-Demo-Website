from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_url_path='', static_folder='ModuleA')
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the uploads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def serve_index():
    return send_from_directory('ModuleA', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return jsonify({'message': 'Image uploaded successfully', 'filename': filename}), 200

if __name__ == '__main__':
    app.run(debug=True)
