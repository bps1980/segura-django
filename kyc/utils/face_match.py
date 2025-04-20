import cv2
import numpy as np

def compare_faces(id_image_path, selfie_image_path):
    try:
        # Load images
        id_img = cv2.imread(id_image_path)
        selfie_img = cv2.imread(selfie_image_path)

        # Convert to grayscale
        id_gray = cv2.cvtColor(id_img, cv2.COLOR_BGR2GRAY)
        selfie_gray = cv2.cvtColor(selfie_img, cv2.COLOR_BGR2GRAY)

        # Load OpenCV face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        id_faces = face_cascade.detectMultiScale(id_gray, 1.3, 5)
        selfie_faces = face_cascade.detectMultiScale(selfie_gray, 1.3, 5)

        if len(id_faces) == 0 or len(selfie_faces) == 0:
            return False, "Face not detected in one or both images."

        # Compare image histograms (basic match metric)
        id_hist = cv2.calcHist([id_gray], [0], None, [256], [0, 256])
        selfie_hist = cv2.calcHist([selfie_gray], [0], None, [256], [0, 256])
        score = cv2.compareHist(id_hist, selfie_hist, cv2.HISTCMP_CORREL)

        return (score > 0.6), f"Similarity Score: {score:.2f}"
    except Exception as e:
        return False, f"OpenCV error: {str(e)}"
