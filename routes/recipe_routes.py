from flask import Blueprint, session, render_template
from models.recipe_model import match_recipes_from_json

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/recipes')
def suggest_recipes():
    user_ingredients = session.get("guest_ingredients", [])

    matched = match_recipes_from_json(user_ingredients)

    return render_template("recipes.html", recipes=matched)
