import json
import os
import random

def load_recipes():
    data_path = os.path.join("data", "recipes.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_random_matching_recipe(user_ingredients, preferred_region=None):
    user_set = set(i.lower() for i in user_ingredients)
    recipes = load_recipes()

    scored_matches = []

    for recipe in recipes:
        recipe_ingredients = set(i.lower() for i in recipe.get("ingredients", []))
        match_score = len(user_set & recipe_ingredients)
        
        if match_score == 0:
            continue  # Skip if no overlap

        region_bonus = 1 if preferred_region and recipe.get("region") == preferred_region else 0
        total_score = match_score + region_bonus

        scored_matches.append((total_score, recipe))

    if not scored_matches:
        return None

    # Get the highest score
    max_score = max(score for score, _ in scored_matches)

    # Filter recipes with that score
    top_matches = [r for score, r in scored_matches if score == max_score]

    # Randomly select one of them
    return random.choice(top_matches)

