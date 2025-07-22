import json
import os
import random
from datetime import datetime, timedelta
from difflib import SequenceMatcher

def is_similar(a, b, threshold=0.85):
    return SequenceMatcher(None, a, b).ratio() >= threshold

def normalize(word):
    word = word.strip().lower()
    if word.endswith("s"):
        word = word[:-1]
    return word


def load_recipes():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "recipes.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_random_matching_recipe(user_ingredients, preferred_region=None, preferred_meal_type=None):
    user_set = set(normalize(i) for i in user_ingredients if i.strip())
    recipes = load_recipes()
    scored_matches = []

    for recipe in recipes:
        recipe_ingredients = set(normalize(i) for i in recipe.get("ingredients", []))

        match_score = sum(
            1 for u_ing in user_set
            for r_ing in recipe_ingredients
            if u_ing == r_ing or is_similar(u_ing, r_ing)
        )

        if match_score == 0:
            continue

        region_bonus = 1 if preferred_region and recipe.get("region") == preferred_region else 0
        meal_type_bonus = 1 if preferred_meal_type and recipe.get("meal_type") == preferred_meal_type else 0
        total_score = match_score + region_bonus + meal_type_bonus
        total_score = match_score + region_bonus

        scored_matches.append((total_score, recipe))
        print(f"[DEBUG] User: {user_set}, Recipe: {recipe['name']}, Match Score: {match_score}")

    if not scored_matches:
        return None

    max_score = max(score for score, _ in scored_matches)
    top_matches = [r for score, r in scored_matches if score == max_score]
    return random.choice(top_matches)


def find_available_recipes_for_user(user_ingredients, preferred_region, preferred_meal_type, recent_recipes):
    user_set = set(normalize(i) for i in user_ingredients if i.strip())
    all_recipes = load_recipes()
    scored_matches = []

    for recipe in all_recipes:
        if recipe["name"] in recent_recipes:
            continue

        recipe_ingredients = set(normalize(i) for i in recipe["ingredients"])

        match_score = sum(
            1 for u_ing in user_set
            for r_ing in recipe_ingredients
            if u_ing == r_ing or is_similar(u_ing, r_ing)
        )

        if match_score == 0:
            continue

        region_bonus = 1 if preferred_region and recipe.get("region") == preferred_region else 0
        meal_type_bonus = 1 if preferred_meal_type and recipe.get("meal_type") == preferred_meal_type else 0
        total_score = match_score + region_bonus

        scored_matches.append((total_score, recipe))
        print(f"[DEBUG] User: {user_set}, Recipe: {recipe['name']}, Match Score: {match_score}")

    scored_matches.sort(reverse=True, key=lambda x: x[0])
    return [r for _, r in scored_matches][:5]

def find_best_matching_recipes(user_ingredients, preferred_region=None, preferred_meal_type=None):
    user_set = set(normalize(i) for i in user_ingredients if i.strip())
    all_recipes = load_recipes()
    scored_matches = []

    for recipe in all_recipes:
        recipe_ingredients = set(normalize(i) for i in recipe.get("ingredients", []))

        match_score = sum(
            1 for u_ing in user_set
            for r_ing in recipe_ingredients
            if u_ing == r_ing or is_similar(u_ing, r_ing)
        )

        if match_score == 0:
            continue

        region_bonus = 1 if preferred_region and recipe.get("region", "").lower() == preferred_region.lower() else 0
        meal_type_bonus = 1 if preferred_meal_type and recipe.get("meal_type", "").lower() == preferred_meal_type.lower() else 0

        
        total_score = match_score + region_bonus + meal_type_bonus  # ✅ fixed

        scored_matches.append((total_score, recipe))
        print(f"[DEBUG] User: {user_set}, Recipe: {recipe['name']}, Score: {total_score}")

    scored_matches.sort(reverse=True, key=lambda x: x[0])
    return [r for _, r in scored_matches]



def log_meal(mongo, user_id, day, meal_type, recipe_name):
    week_number = datetime.utcnow().isocalendar()[1]
    existing = mongo.db.mealplans.find_one({
        "user_id": user_id,
        "week_number": week_number
    })

    if existing:
        mongo.db.mealplans.update_one(
            {"_id": existing["_id"]},
            {"$push": {"meals": {
                "day": day,
                "meal_type": meal_type,
                "recipe_name": recipe_name
            }}}
        )
    else:
        mongo.db.mealplans.insert_one({
            "user_id": user_id,
            "week_number": week_number,
            "meals": [{
                "day": day,
                "meal_type": meal_type,
                "recipe_name": recipe_name
            }]
        })

def get_meals_this_week(mongo, user_id):
    week_number = datetime.utcnow().isocalendar()[1]
    return list(mongo.db.mealplans.find({
        "user_id": user_id,
        "week_number": week_number
    }))

