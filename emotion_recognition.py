# emotion_detection.py
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np

# loading machine learning model for emotion recognition
model = load_model('ModuleA/Resources/emotion_recognition.keras')

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))  # Resize it to the expected size for the model
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR image to RGB
    img = img / 255.0  # Scale pixel values to [0, 1]
    img = np.expand_dims(img, axis=0)  # Expand dimensions to represent batch size
    return img

def detect_emotion(image_path):
    processed_image = preprocess_image(image_path)
    if processed_image is not None:
        predictions = model.predict(processed_image)
        emotions = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
        status = emotions[np.argmax(predictions)]
        print(status)
        return status
    else:
        print("Processing failed.")
        return None

if __name__ == "__main__":
    image_path = 'uploads/face_roi.png'
    detect_emotion(image_path)
