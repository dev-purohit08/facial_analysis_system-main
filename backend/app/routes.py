from fastapi import APIRouter
from pydantic import BaseModel
import cv2
import os
import numpy as np
import mediapipe as mp
import time
from app.face_store import save_face
from app.detector import detector
from app.utils import decode_base64_image, get_face_vector, eye_aspect_ratio
from app.face_store import known_vectors, known_names
from app.config import LEFT_EYE, RIGHT_EYE, KNOWN_FACES_DIR, EMOTION_HOLD_FRAMES

router = APIRouter()

current_emotion = "Neutral"
emotion_counter = 0
is_drowsy = False

class FrameData(BaseModel):
    image: str
    mode: str

class CaptureData(BaseModel):
    image: str


@router.post("/process_frame")
def process_frame(data: FrameData):
    global current_emotion, emotion_counter, is_drowsy

    frame = decode_base64_image(data.image)
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)

    if result.face_landmarks:
        landmarks = result.face_landmarks[0]
        points = np.array([[int(lm.x * w), int(lm.y * h)] for lm in landmarks])
        face_vec = get_face_vector(landmarks)

        if data.mode == "landmark":
            for (x, y) in points:
                cv2.circle(frame, (x, y), 1, (0,255,0), -1)

        elif data.mode == "emotion":
            detected = "Neutral"
            if result.face_blendshapes:
                scores = {b.category_name: b.score for b in result.face_blendshapes[0]}
                threshold = 0.20

                emotion_scores = {
                    "Happy": scores.get("mouthSmileLeft",0) + scores.get("mouthSmileRight",0),
                    "Sad": scores.get("mouthFrownLeft",0) + scores.get("mouthFrownRight",0),
                    "Angry": scores.get("browDownLeft",0) + scores.get("browDownRight",0),
                    "Surprised": scores.get("jawOpen",0)
                }

                best = max(emotion_scores, key=emotion_scores.get)
                if emotion_scores[best] > threshold:
                    detected = best

            if detected == current_emotion:
                emotion_counter = 0
            else:
                emotion_counter += 1
                if emotion_counter >= EMOTION_HOLD_FRAMES:
                    current_emotion = detected
                    emotion_counter = 0

            cv2.putText(frame, f"Emotion: {current_emotion}", (30,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        elif data.mode == "drowsy":
            left_eye = points[LEFT_EYE]
            right_eye = points[RIGHT_EYE]
            ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2

            if ear < 0.20:
                is_drowsy = True
                cv2.putText(frame, "DROWSINESS ALERT!", (30,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
            else:
                is_drowsy = False
                cv2.putText(frame, "Eyes Open", (30,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        elif data.mode == "recognition":
            name = "Unknown"
            min_dist = 999

            for vec, person in zip(known_vectors, known_names):
                dist = np.linalg.norm(face_vec - vec)
                if dist < min_dist:
                    min_dist = dist
                    name = person

            if min_dist > 0.6:
                name = "Unknown"

            cv2.putText(frame, f"Person: {name}", (30,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    _, buffer = cv2.imencode(".jpg", frame)
    processed = buffer.tobytes()

    import base64
    processed = base64.b64encode(processed).decode("utf-8")

    return {"image": f"data:image/jpeg;base64,{processed}", "drowsy": is_drowsy}


@router.post("/capture/{person_name}")
def capture_photo(person_name: str, data: CaptureData):

    frame = decode_base64_image(data.image)
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)

    if not result.face_landmarks:
        return {"status": "no_face_detected"}

    filename = f"{person_name}_{int(time.time())}.jpg"
    path = os.path.join(KNOWN_FACES_DIR, filename)

    success = cv2.imwrite(path, frame)
    print("Saving to:", path, "success:", success)

    vec = get_face_vector(result.face_landmarks[0])
    known_vectors.append(vec)
    known_names.append(person_name)

    return {"status": "saved", "file": filename}

