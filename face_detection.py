# face_detection.py
import cv2

# Load the Haar Cascade for face detection


def detect_and_save_face(image_path):
    face_cascade = cv2.CascadeClassifier('Website/Resources/haarcascade_frontalface_default (1).xml')
    # Load the image
    image_path = ('uploads/captured_image.png')
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        print("No face detected.")
        return False
    
    for (x, y, w, h) in faces:
        # Save the image with detected faces marked
        detected_faces_img = img.copy()
        cv2.rectangle(detected_faces_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imwrite('uploads/face_detected.png', detected_faces_img)
        
        face_roi = img[y:y+h, x:x+w]
        cv2.imwrite('uploads/face_roi.png', face_roi)
        break  # Only interested in the first face for this scenario
    
    return True

if __name__ == "__main__":
    image_path = 'uploads/captured_image.png'  
    success = detect_and_save_face(image_path)

