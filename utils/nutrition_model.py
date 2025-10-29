import pandas as pd
from rapidfuzz import process, fuzz
from utils.helpers import parse_quantity

class NutritionEngine:
    def __init__(self, data_path="food_nutrition.csv"):
        self.df = pd.read_csv(data_path)
        # expect columns: name, serving_size_g, calories, protein_g, carbs_g, fat_g
        self.names = self.df["name"].tolist()

    def match_food(self, name):
        # use rapidfuzz to find best match
        match = process.extractOne(name, self.names, scorer=fuzz.WRatio, score_cutoff=60)
        if match:
            matched_name = match[0]
            row = self.df[self.df["name"] == matched_name].iloc[0].to_dict()
            return row
        return None

    def scale_nutrients(self, row, quantity, qtype):
        # assume row["serving_size_g"] exists
        base_g = row.get("serving_size_g", 100)
        if qtype == "g":
            factor = quantity / base_g
        elif qtype == "cup":
            # simplistic assumption: 1 cup = base_g grams
            factor = quantity
        elif qtype == "pieces" or qtype == "unit":
            factor = quantity
        else:
            factor = 1.0
        return {
            "calories": float(row.get("calories",0)) * factor,
            "protein": float(row.get("protein_g",0)) * factor,
            "carbs": float(row.get("carbs_g",0)) * factor,
            "fat": float(row.get("fat_g",0)) * factor
        }

    def compute_meal_nutrition(self, foods):
        breakdown = []
        totals = {"calories":0,"protein":0,"carbs":0,"fat":0}
        for f in foods:
            name = f.get("item")
            qty_text = f.get("quantity","")
            qty, qtype = parse_quantity(qty_text)
            matched = self.match_food(name)
            if matched is None:
                # Skip unknowns for demo
                continue
            scaled = self.scale_nutrients(matched, qty if qty is not None else 1, qtype)
            breakdown.append({
                "item": f"{matched['name']} ({qty_text})",
                "calories": round(scaled["calories"],2),
                "protein": round(scaled["protein"],2),
                "carbs": round(scaled["carbs"],2),
                "fat": round(scaled["fat"],2)
            })
            totals["calories"] += scaled["calories"]
            totals["protein"] += scaled["protein"]
            totals["carbs"] += scaled["carbs"]
            totals["fat"] += scaled["fat"]
        return {
            "total_calories": round(totals["calories"],2),
            "macros": {"protein": round(totals["protein"],2), "carbs": round(totals["carbs"],2), "fat": round(totals["fat"],2)},
            "breakdown": breakdown
        }
