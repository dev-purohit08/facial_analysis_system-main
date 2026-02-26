Real Time Facial Analysis System

A full-stack, Dockerized AI web application built using FastAPI, MediaPipe, and OpenCV that performs real-time facial analysis directly in the browser.

The system supports:

Facial Landmark Detection

Emotion Detection

Drowsiness Detection (with Browser Alarm)

Face Recognition

Face Enrollment

The application is fully browser-based and cloud deployable.

🚀 Live Demo

(Deployment link will be added here)

🏗 System Architecture

Frontend:

HTML

CSS

JavaScript

Web Camera API (getUserMedia)

Nginx (for static serving)

Backend:

FastAPI

MediaPipe Face Landmarker

OpenCV

NumPy

Deployment:

Docker & Docker Compose

Cloud ready (Render / AWS / EC2 / Railway)

🧠 Features
1️⃣ Facial Landmark Detection

Detects and visualizes 468 facial landmarks in real time using MediaPipe Face Landmarker.

2️⃣ Emotion Detection

Classifies facial expressions into:

Happy

Sad

Angry

Surprised

Neutral

Includes smoothing logic to prevent rapid flickering between emotions.

3️⃣ Drowsiness Detection

Uses Eye Aspect Ratio (EAR) to detect eye closure.

Detects closed eyes in real time

Triggers browser-based alarm sound

Alarm automatically stops when eyes reopen

Alarm is handled entirely on the frontend.

4️⃣ Face Recognition

Matches detected faces against enrolled users using landmark vector similarity.

5️⃣ Face Enrollment

Allows users to:

Capture a face image

Save it to the backend

Automatically add it to recognition memory

Includes success/error toast notifications.

📂 Project Structure
facial-analysis-system/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── detector.py
│   │   ├── face_store.py
│   │   ├── utils.py
│   │   ├── config.py
│   │   └── models/
│   │       └── face_landmarker.task
│   │
│   ├── known_faces/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── static/
│   │   ├── index.html
│   │   └── alarm.mp3
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
🐳 Docker Setup (Recommended)
Run with Docker Compose

From project root:

docker compose build
docker compose up

Backend runs on:

http://localhost:8000

Frontend runs on:

http://localhost:3000
💻 Local Development (Without Docker)
1️⃣ Clone Repository
git clone https://github.com/dev-purohit08/facial-analysis-system-main.git
cd facial-analysis-system/backend
2️⃣ Create Virtual Environment
python -m venv .venv
Activate

Windows:

.venv\Scripts\activate

Mac/Linux:

source .venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run Backend
uvicorn app.main:app --reload

Open frontend manually via frontend/static/index.html.

🌐 Cloud Deployment

The backend can be deployed on:

Render

Railway

AWS EC2

Any Docker-supported cloud platform

Start command:

uvicorn app.main:app --host 0.0.0.0 --port 10000

Python Version:

3.10.x
⚠️ Important Notes

Browser camera access is required.

Backend does NOT use server webcam.

Alarm sound is triggered in frontend only.

face_landmarker.task must exist in:

backend/app/models/

known_faces/ is mounted as a Docker volume.

🔒 Security Notes

No biometric data is stored permanently unless images are saved in known_faces/.

For production deployment, HTTPS is required for camera access.

📈 Future Improvements

Persistent face embedding storage (database instead of memory)

GPU acceleration support

User authentication

Rate limiting

CI/CD pipeline

👨‍💻 Author

Dev Purohit
MCA Final Year Project
Real Time Facial Analysis System
