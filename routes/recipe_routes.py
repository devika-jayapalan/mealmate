from flask import Blueprint, session, render_template, current_app
from models.recipe_model import match_recipes

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/recipes')
def recipes():
    mongo = current_app.mongo

    user_id = session.get('user_id')
    ingredients = []

    if user_id:
        # If logged in, fetch ingredients from DB
        user_ingredients = mongo.db.ingredients.find({"user_id": user_id})
        ingredients = [doc['ingredient'] for doc in user_ingredients]
    else:
        # If guest, fetch from session
        ingredients = session.get('guest_ingredients', [])

    suggested = match_recipes(mongo, ingredients)
    return render_template('recipes.html', recipes=suggested)
