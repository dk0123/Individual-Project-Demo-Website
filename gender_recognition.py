import tensorflow as tf
import cv2
import numpy as np
import random

seed_constant = 49
random.seed(seed_constant)

# Disable GPU (if needed)
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Load the pre-trained gender recognition model
gender_model = tf.keras.models.load_model('ModuleA/Resources/gender_model.keras')

# Load the face ROI image
face_roi = cv2.imread('uploads/face_roi.jpg')

# Preprocess the image
face_roi = cv2.resize(face_roi, (48, 48)) # Normalize pixel values to [0, 1]
face_roi = np.expand_dims(face_roi, axis=0)  # Add batch dimension

# Make predictions
predictions = gender_model.predict(face_roi)
print("predictions:", predictions)

# Interpret the predictions
gender_labels = ['Male', 'Female']
predicted_gender = gender_labels[np.argmax(predictions)]
confidence = predictions[0][np.argmax(predictions)]

print("Predicted Gender:", predicted_gender)
print("Confidence:", confidence)