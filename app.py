from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from utils.diet_model import generate_7day_plan
from utils.nutrition_model import NutritionEngine

app = FastAPI(title="Diet Recommendation & Nutrition API")

# 👇 Add this block to enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["http://localhost:19006"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nutrition_engine = NutritionEngine(data_path="food_nutrition.csv")

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

@app.post("/diet-plan")
def diet_plan(user: UserInput):
    plan = generate_7day_plan(user.dict())
    return {"daily_plan": plan}

@app.post("/nutrition")
def nutrition(req: FoodRequest):
    result = nutrition_engine.compute_meal_nutrition([f.dict() for f in req.foods])
    return {"meal_nutrition": result}

@app.get("/ping")
def ping():
    return {"status": "ok"}
