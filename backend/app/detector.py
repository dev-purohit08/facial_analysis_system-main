from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from app.config import MODEL_PATH

base_options = python.BaseOptions(model_asset_path=str(MODEL_PATH))

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    num_faces=1,
)

detector = vision.FaceLandmarker.create_from_options(options)