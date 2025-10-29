# Backend - FastAPI for Diet Recommendation & Nutrition

## Overview
This FastAPI backend exposes two endpoints:
- `POST /diet-plan` - Generate a 7-day diet plan based on user parameters.
- `POST /nutrition` - Compute nutrition breakdown for provided foods and quantities.

## Run locally
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8080
```

## Docker & Google Cloud Run (summary)
1. Build docker image:
```bash
docker build -t gcr.io/PROJECT-ID/diet-backend:latest .
```

2. Push to Artifact Registry / Container Registry and deploy to Cloud Run (or use Cloud Build).
See Google Cloud docs — replace `PROJECT-ID` and region as needed.
# ai-dietplan
# ai-dietplan
