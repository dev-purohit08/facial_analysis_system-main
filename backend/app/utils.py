import cv2
import base64
import numpy as np

def get_face_vector(landmarks):
    vec = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
    return vec / np.linalg.norm(vec)

def eye_aspect_ratio(eye_points):
    A = np.linalg.norm(eye_points[1] - eye_points[5])
    B = np.linalg.norm(eye_points[2] - eye_points[4])
    C = np.linalg.norm(eye_points[0] - eye_points[3])
    return (A + B) / (2.0 * C)

def decode_base64_image(data):
    header, encoded = data.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
