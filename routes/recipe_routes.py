from flask import Blueprint, session, render_template, request, redirect, current_app
from datetime import datetime
from models.recipe_model import find_best_matching_recipes, log_meal, get_meals_this_week, find_random_matching_recipe

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/recipes')
def suggest_recipes():
    user_id = session.get("user_id")
    region = session.get("region_preference")
    meal_type = session.get("meal_type_preference") 
    mongo = current_app.mongo
    print(f"[DEBUG] session user_id: {user_id}")

    if not user_id:
        # Guest flow
        ingredients = session.get("guest_ingredients", [])
        matching_recipes = find_best_matching_recipes(ingredients, region, meal_type)  

        session['guest_recipe_queue'] = matching_recipes
        session['recipe_pointer'] = 0

        return render_template("recipes.html", recipes=[matching_recipes[0]] if matching_recipes else [])

    else:
        # Logged-in flow
        ingredients = [doc["ingredient"] for doc in mongo.db.ingredients.find({"user_id": user_id})]
        past_meals = get_meals_this_week(mongo, user_id)
        used_names = {meal["recipe_name"] for entry in past_meals for meal in entry["meals"]}

        suggestions = find_best_matching_recipes(ingredients, region, meal_type)  # ← Include meal_type
        fresh_suggestions = [r for r in suggestions if r["name"] not in used_names]

        session['user_recipe_queue'] = fresh_suggestions
        session['recipe_pointer'] = 0

        print(f"[DEBUG] Matching recipes for user: {fresh_suggestions[:1]}")

        return render_template("recipes.html", recipes=fresh_suggestions[:1])


@recipe_bp.route('/select_recipe', methods=['POST'])
def select_recipe():
    recipe_name = request.form.get("recipe_name")
    meal_type = request.form.get("meal_type", "custom")  # Optional input
    user_id = session.get("user_id")

    if not recipe_name or not user_id:
        return redirect("/recipes")  # Fail-safe fallback

    mongo = current_app.mongo

    log_meal(mongo, user_id, day=datetime.utcnow().strftime("%A"), meal_type=meal_type, recipe_name=recipe_name)
    
    return render_template("thank_you.html", recipe_name=recipe_name)
@recipe_bp.route('/next_recipe')
def next_recipe():
    user_id = session.get("user_id")
    queue_key = "user_recipe_queue" if user_id else "guest_recipe_queue"

    recipe_queue = session.get(queue_key, [])
    pointer = session.get("recipe_pointer", 0)

    if not recipe_queue:
        return redirect("/recipes")  # fallback

    pointer = (pointer + 1) % len(recipe_queue)
    session["recipe_pointer"] = pointer

    return render_template("recipes.html", recipes=[recipe_queue[pointer]])
