import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent  # /app/app

# keep known_faces mounted volume path exactly as your compose specifies
KNOWN_FACES_DIR = str(APP_DIR.parent / "known_faces")  # /app/known_faces
MODEL_PATH = str(APP_DIR / "models" / "face_landmarker.task")

os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
EMOTION_HOLD_FRAMES = 5