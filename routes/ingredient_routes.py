from flask import Blueprint, session, request, redirect, render_template, current_app
import json
from datetime import datetime

ingredient_bp = Blueprint('ingredient', __name__)

@ingredient_bp.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    mongo = current_app.mongo
    user_id = session.get('user_id')  # may be None

    if request.method == 'POST':
        region = request.form.get("region") or session.get("region_preference")
        if region:
            session["region_preference"] = region

        meal_type = request.form.get("meal_type") or session.get("meal_type_preference")
        if meal_type:
            session["meal_type_preference"] = meal_type


        ingredients_json = request.form.get('ingredients', '[]')
        try:
            ingredients_list = json.loads(ingredients_json)
        except Exception:
            ingredients_list = []

        clean_ingredients = [i.strip().lower() for i in ingredients_list if i.strip()]
        session['guest_ingredients'] = clean_ingredients

        if not user_id:
            # Guest
            session.pop("used_recipes", None)
            session.pop("guest_recipe_queue", None)
            session.pop("recipe_pointer", None)
        else:
            # Logged-in
            mongo.db.ingredients.delete_many({"user_id": user_id})
            for item in ingredients_list:
                mongo.db.ingredients.insert_one({
                    "user_id": user_id,
                    "ingredient": item,
                    "region": region,
                    "meal_type": meal_type,  # optional storage
                    "submitted_at": datetime.utcnow()
                })
                print(f"[DEBUG] Saving ingredient: {item}")

        return redirect('/recipes')

    return render_template('ingredients.html')


    return render_template('ingredients.html')
