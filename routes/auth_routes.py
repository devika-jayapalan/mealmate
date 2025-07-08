from flask import Blueprint, request, render_template, redirect, session, current_app
from bson.objectid import ObjectId

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mongo = current_app.mongo

        # Check if user exists
        user = mongo.db.users.find_one({"email": "email"})
        if not user:
            # Create new user
            user_id = mongo.db.users.insert_one({
                "name": name,
                "email": email,
            }).inserted_id
        else:
            user_id = user['_id']

        # Store user ID in session
        session['user_id'] = str(user_id)
        return redirect('/ingredients')

    return render_template('login.html')
