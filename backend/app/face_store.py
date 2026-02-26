import os
import cv2
import mediapipe as mp
import time
from app.detector import detector
from app.config import KNOWN_FACES_DIR
from app.utils import get_face_vector

known_vectors = []
known_names = []

os.makedirs(KNOWN_FACES_DIR, exist_ok=True)


def load_known_faces():
    known_vectors.clear()
    known_names.clear()

    for file in os.listdir(KNOWN_FACES_DIR):
        path = os.path.join(KNOWN_FACES_DIR, file)
        name = os.path.splitext(file)[0]

        img = cv2.imread(path)
        if img is None:
            continue

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect(mp_image)

        if result.face_landmarks:
            vec = get_face_vector(result.face_landmarks[0])
            known_vectors.append(vec)
            known_names.append(name)


def save_face(person_name: str, frame):
    filename = f"{person_name}_{int(time.time())}.jpg"
    path = os.path.join(KNOWN_FACES_DIR, filename)

    cv2.imwrite(path, frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)

    if result.face_landmarks:
        vec = get_face_vector(result.face_landmarks[0])
        known_vectors.append(vec)
        known_names.append(person_name)

    return filename