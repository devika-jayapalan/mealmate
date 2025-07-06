from flask import Blueprint, session, request, redirect, render_template, current_app
from datetime import datetime

ingredient_bp = Blueprint('ingredient', __name__)

@ingredient_bp.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    mongo = current_app.mongo
    user_id = session.get('user_id')  # may be None

    if request.method == 'POST':
        raw_input = request.form.get('ingredients')
        ingredients = [i.strip() for i in raw_input.split('\n') if i.strip()]

        # Only save to DB if user is logged in
        if user_id:
            for item in ingredients:
                mongo.db.ingredients.insert_one({
                    "user_id": user_id,
                    "ingredient": item,
                    "submitted_at": datetime.utcnow()
                })

        # Store ingredients in temporarily for guests
        session['guest_ingredients'] = ingredients
        return redirect('/recipes')

    return render_template('ingredients.html')

