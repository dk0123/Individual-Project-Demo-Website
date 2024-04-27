from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from recommendations import main as get_movie_recommendations

app = Flask(__name__, static_url_path='', static_folder='ModuleA')
app.config['UPLOAD_FOLDER'] = 'uploads'

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
    # Trigger recommendation after image is saved and processed
    recommendations = get_movie_recommendations()
    return jsonify({'message': 'Image uploaded successfully', 'filename': filename, 'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
