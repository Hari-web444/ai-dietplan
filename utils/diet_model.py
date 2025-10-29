import math
from typing import Dict, Any, List
# Simple calorie calculator and meal planner for demo purposes

def bmr_mifflin(weight_kg, height_cm, age, gender="male"):
    # Using Mifflin - St Jeor (gender neutral assume male/female not provided)
    if gender == "male":
        return 10*weight_kg + 6.25*height_cm - 5*age + 5
    else:
        return 10*weight_kg + 6.25*height_cm - 5*age - 161

def adjust_calories_for_goal(bmr, goal):
    if goal.lower() == "weight loss":
        return int(bmr * 0.8)
    elif goal.lower() == "muscle gain":
        return int(bmr * 1.15)
    else:
        return int(bmr * 1.0)

# Sample regional meal templates (very small for demo)
MEAL_TEMPLATES = {
    "South India": {
        "Vegetarian": {
            "breakfast": [("Idli (2)", 250), ("Sambar (1 cup)", 120)],
            "lunch": [("Brown rice (1 cup)", 400), ("Sambar (1 cup)", 120), ("Curd (100g)", 60)],
            "dinner": [("Chapathi (2)", 200), ("Paneer curry (1 cup)", 300)],
            "snacks": ["Buttermilk", "Fruits"]
        },
        "Non-Vegetarian": {
            "breakfast": [("Egg omelette (2)", 220), ("Toast", 120)],
            "lunch": [("Rice (1 cup)", 400), ("Grilled fish (150g)", 300), ("Veg", 100)],
            "dinner": [("Chapathi (2)", 200), ("Chicken curry (1 cup)", 350)],
            "snacks": ["Nuts", "Fruit"]
        }
    }
}

def generate_day(meals, target_cal):
    day = {"total_calories": 0, "meals": {}, "snacks": meals.get("snacks", [])}
    total = 0
    for mname, items in [("breakfast", meals["breakfast"]), ("lunch", meals["lunch"]), ("dinner", meals["dinner"]) ]:
        item_names = [i[0] for i in items]
        cals = sum(i[1] for i in items)
        day["meals"][mname] = {"items": item_names, "calories": cals}
        total += cals
    day["total_calories"] = total
    return day

def generate_7day_plan(user: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Basic BMR estimate
    bmr = bmr_mifflin(user["current_weight_kg"], user["height_cm"], user["age"], gender="male")
    target_cal = adjust_calories_for_goal(bmr, user.get("goal", "Maintenance"))
    region = user.get("region", "South India")
    cuisine = user.get("cuisine_preference", "Vegetarian")
    templates = MEAL_TEMPLATES.get(region, MEAL_TEMPLATES["South India"]).get(cuisine, MEAL_TEMPLATES["South India"]["Vegetarian"])
    week = {}
    for i in range(7):
        day_name = f"day_{i+1}"
        week[day_name] = generate_day(templates, target_cal)
    return week
