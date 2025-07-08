import json
from pathlib import Path

def load_recipes():
    with open(Path("data/recipes.json"), "r") as f:
        return json.load(f)

def match_recipes_from_json(available_ingredients):
    available_set = set(i.lower() for i in available_ingredients)
    recipes = load_recipes()
    matches = []

    for recipe in recipes:
        recipe_ingredients = set(i.lower() for i in recipe["ingredients"])
        if recipe_ingredients.issubset(available_set):
            matches.append(recipe)
    
    return matches
