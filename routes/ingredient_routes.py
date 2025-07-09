from flask import Blueprint, session, request, redirect, render_template, current_app
import json
from datetime import datetime

ingredient_bp = Blueprint('ingredient', __name__)

@ingredient_bp.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    mongo = current_app.mongo
    user_id = session.get('user_id')  # may be None

    if request.method == 'POST':
        ingredients_json = request.form.get('ingredients', '[]')
        try:
            ingredients_list = json.loads(ingredients_json)
        except Exception:
            ingredients_list = []

        region = request.form.get('region')
        session['region_preference'] = region  # store for recipe matching
        session['guest_ingredients'] = ingredients_list

        if not user_id:
            # 👇 Reset recipe history for guests (do not apply no-repeat rule)
            session.pop("used_recipes", None)
        else:
            # 👇 Save ingredients to DB for logged-in users
            for item in ingredients_list:
                mongo.db.ingredients.insert_one({
                    "user_id": user_id,
                    "ingredient": item,
                    "region": region,
                    "submitted_at": datetime.utcnow()
                })

        return redirect('/recipes')

    return render_template('ingredients.html')
