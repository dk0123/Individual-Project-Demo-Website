#importing necessary liabraries
import tensorflow as tf
import cv2
import os
import numpy as np
import random
from tensorflow import keras
from tensorflow.keras import layers

from tensorflow.keras.optimizers.legacy import Adam

from face_detection import detect_and_save_face


image_path = 'uploads/captured_image.png'  
face_roi_image = detect_and_save_face(image_path)


# loading machine learning model for emotion recognition
emotion_model = tf.keras.models.load_model('ModuleA/Resources/emotion_recognition.keras')

# loading the ML model for Gender Recognition.
gender_model = tf.keras.models.load_model('ModuleA/Resources/gender_model.keras')

# loading the ML model for Age Recognition.
age_model = tf.keras.models.load_model('ModuleA/Resources/age_model.keras')


# For Gender REcognition
final_image2 = cv2.imread('uploads/face_roi.png')
final_image2 = cv2.resize(final_image2,(224,224))
final_image2 = np.expand_dims(final_image2,axis=0) # need a fourth dimenstion

Gender_Prediction = gender_model.predict(final_image2)

#Printing Confidence of Gender Predicted
#print(Gender_Prediction)
#Printign the Gender Predicted
Predicted_Gender = (np.argmax(Gender_Prediction))
if (Predicted_Gender==0):
  Predicted_Gender = ("Male")
elif (Predicted_Gender==1):
  Predicted_Gender = ("Female")

#print(Predicted_Gender)


#For Age Recognition Model
from tensorflow.keras.applications.resnet import preprocess_input
# Load the image file
final_image3 = cv2.imread('uploads/face_roi.png')

final_image3 = cv2.cvtColor(final_image3, cv2.COLOR_BGR2RGB)
final_image3 = cv2.resize(final_image3,(224,224))
final_image3 = np.expand_dims(final_image3, axis=0)  # Add a 4th dimension
final_image3 = preprocess_input(final_image3)


Age_Prediction = age_model.predict(final_image3)
#Print the Age Predicted
#print(Age_Prediction)


#For emotion detection
final_image4 = cv2.imread('uploads/face_roi.png')
final_image4 = cv2.resize(final_image4,(224,224))
final_image4 = np.expand_dims(final_image4, axis=0)  # Add a 4th dimension

final_image4 = final_image4/255.0 # normalizing

Predictions = emotion_model.predict(final_image4)

#Print the Emotion Predicted
#print(Predictions)

#Print the max number 
np.argmax(Predictions)

if (np.argmax(Predictions)==0):
  status = "Angry"
elif (np.argmax(Predictions)==1):
  status = "Disgust"
elif (np.argmax(Predictions)==2):
  status = "Fear"
elif (np.argmax(Predictions)==3):
  status = "Happy"
elif (np.argmax(Predictions)==4):
  status = "Sad"
elif (np.argmax(Predictions)==5):
  status = "Surprise"
elif (np.argmax(Predictions)==6):
  status = "Neutral"

#print(status)

def get_demographics():
    return Predicted_Gender, status, Age_Prediction
