import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from utils.diet_model import generate_7day_plan
from utils.nutrition_model import NutritionEngine


# ✅ Initialize FastAPI app
app = FastAPI(title="AI Diet Plan API")

# ✅ Enable CORS (must come right after FastAPI init)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:19006",  # Expo local dev
        "https://ai-dietplan-921d.onrender.com"  # optional self-call
    ],
    allow_credentials=True,
    allow_methods=["*"],  # include OPTIONS to allow preflight
    allow_headers=["*"],
)

# ✅ Ensure file path works on Render
DATA_PATH = os.path.join(os.path.dirname(__file__), "food_nutrition.csv")
nutrition_engine = NutritionEngine(data_path=DATA_PATH)


# ✅ Define models
class UserInput(BaseModel):
    name: str
    age: int
    goal: str
    height_cm: float
    current_weight_kg: float
    target_weight_kg: Optional[float] = None
    health_conditions: Optional[List[str]] = []
    region: Optional[str] = "South India"
    cuisine_preference: Optional[str] = "Vegetarian"
    allergies: Optional[List[str]] = []


class FoodItem(BaseModel):
    item: str
    quantity: str


class FoodRequest(BaseModel):
    foods: List[FoodItem]


# ✅ Routes

@app.get("/")
def root():
    return {
        "message": "✅ AI Diet Plan API is Live and CORS Enabled!",
        "status": "healthy",
        "endpoints": ["/ping", "/diet-plan", "/nutrition"],
    }


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/diet-plan")
def diet_plan(user: UserInput):
    plan = generate_7day_plan(user.dict())
    return {"daily_plan": plan}


@app.post("/nutrition")
def nutrition(req: FoodRequest):
    result = nutrition_engine.compute_meal_nutrition([f.dict() for f in req.foods])
    return {"meal_nutrition": result}
