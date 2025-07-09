from flask import Blueprint, session, render_template
from models.recipe_model import find_random_matching_recipe

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/recipes')
def suggest_recipes():
    user_ingredients = session.get("guest_ingredients", [])
    region = session.get("region_preference")

    recipe = find_random_matching_recipe(user_ingredients, region)

    if recipe:
        return render_template("recipes.html", recipes=[recipe])
    else:
        return render_template("recipes.html", recipes=[])
