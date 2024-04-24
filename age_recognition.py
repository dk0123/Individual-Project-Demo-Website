import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
import tensorflow as tf

# Load the pre-trained age model (adjust the path as needed)
model = tf.keras.models.load_model('ModuleA/Resources/age_model.keras')

# Load the image file
img_path = 'uploads/photo.png'
img = cv2.imread(img_path)
#img = cv2cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB

# Resize the image to match the model's expected input size
img = cv2.resize(img, (224, 224))  # Adjust the size based on your model's requirements

# Preprocess the image to prepare it for the model
img = preprocess_input(img)

# Expand the dimensions to match the model's input format
img = np.expand_dims(img, axis=0)

if __name__ == "__main__":
    age = model.predict(img)
    print("Predicted Age:", age[0][0])