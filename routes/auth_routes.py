from flask import Blueprint, render_template, request, session, redirect, current_app
from models.user_model import get_user_by_email, create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        mongo = current_app.mongo

        user = get_user_by_email(mongo, email)
        if not user:
            user_id = create_user(mongo, name, email)
        else:
            user_id = user['_id']

        session['user_id'] = str(user_id)
        return redirect('/ingredients')

    return render_template('login.html')
