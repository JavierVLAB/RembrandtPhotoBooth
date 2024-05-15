import cv2
import numpy as np
import urllib.request

def load_image_from_url(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def detect_faces(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def apply_rembrandt_style(image, faces):
    for (x, y, w, h) in faces:
        # Apply a mask to create the Rembrandt triangle of light
        mask = np.zeros_like(image)
        cv2.ellipse(mask, (x + w // 2, y + h // 2), (w // 2, h // 2), 0, 0, 360, (255, 255, 255), -1)
        rembrandt_effect = cv2.addWeighted(image, 0.5, mask, 0.5, 0)
        cv2.rectangle(rembrandt_effect, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return rembrandt_effect

# URL of the image
image_url = "https://images.unsplash.com/photo-1580489944761-15a19d654956"
image = load_image_from_url(image_url)
faces = detect_faces(image)
rembrandt_image = apply_rembrandt_style(image, faces)

# Show the final image
cv2.imshow('Rembrandt Style Image', rembrandt_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
