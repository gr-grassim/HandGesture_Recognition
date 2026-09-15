# Hand Gesture Recognition

A real-time, web-based hand gesture recognition system utilizing MediaPipe, Random Forest, and FastAPI.

## Demo / Architecture
The system captures webcam feed from the browser, extracts canonical 63D hand landmarks via MediaPipe HandLandmarker, and sends these features to a FastAPI backend for real-time classification using a trained Random Forest model.

## Key Features
- **Real-Time Inference:** Browser-based webcam integration.
- **Robust Feature Extraction:** 63D coordinate extraction using Google's MediaPipe.
- **Machine Learning Backend:** FastAPI serving a Random Forest classifier.
- **Responsive UI:** Built with React, Vite, and Tailwind CSS.

## Supported Gestures
- `open_palm`
- `fist`
- `pointing`
- `victory`
- `thumbs_up`
- `rock`

*Note: `thumbs_down` and `okay` gestures are currently **not** supported.*

## Dataset
- **Source:** [Hand Gesture Landmarks by Youssef Elebiary](https://www.kaggle.com/datasets/youssefelebiary/hand-gesture-landmarks)
- **License:** MIT
- **Size:** 364 samples

## Evaluation & Model Limitations
- **Test Accuracy:** 1.0 (100%)
- **Test Macro F1:** 1.0 (100%)

> [!WARNING]
> **Important Limitation:** While the evaluation metrics are perfect, this model is **NOT** production-quality. The dataset is extremely small (364 samples) and lacks subject metadata, meaning subject-independent evaluation is unavailable. These results do not guarantee real-world generalization across different hands, lighting, or angles.

## System Architecture / Tech Stack
- **Frontend:** React, Vite, Tailwind CSS, MediaPipe HandLandmarker.
- **Backend:** FastAPI, Python, scikit-learn (Random Forest v2).
- **Deployment (Planned):** Vercel (Frontend), IBM Code Engine (Backend Docker Container).

## Project Structure
```text
HandGesture_Recognition/
├── backend/            # FastAPI server and ML inference logic
├── frontend/           # React + Vite web application
├── ml/                 # Model training, dataset processing, and models
├── docs/               # Project documentation
├── docker-compose.yml  # Local multi-container setup
├── Dockerfile          # Backend Dockerfile
└── ...
```

## Local Setup

### Environment Variables
- Create `.env` in `frontend/` (copy from `.env.example`).
- Set `VITE_API_BASE_URL=http://localhost:8000` (or leave empty to default).

### Running Backend
1. Create and activate a Python virtual environment.
2. `pip install -r backend/requirements.txt`
3. `cd backend && uvicorn app.main:app --reload`

### Running Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

### Docker Instructions
To build and run the backend locally using Docker:
```bash
cd backend
docker build -t handgesture-backend .
docker run -p 8000:8000 handgesture-backend
```

## API Endpoints
- `GET /health` - Health check.
- `GET /api/model-info` - Returns loaded model metadata and classes.
- `POST /api/predict` - Accepts a 63D array of landmarks and returns the predicted gesture and confidence.

## Testing
- **Backend:** Run `pytest backend/tests`
- **Frontend:** Run `npm test` or `npm run test`

## Future Improvements
- Expand dataset with more diverse subjects to improve generalization.
- Support more complex dynamic gestures.
- Add user-level calibration.

## License
MIT License
