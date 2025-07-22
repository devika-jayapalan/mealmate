from flask import Flask, render_template
from flask_pymongo import PyMongo
from routes.auth_routes import auth_bp
from routes.ingredient_routes import ingredient_bp
from routes.recipe_routes import recipe_bp

app = Flask(__name__)
app.secret_key = "secret" 
app.config["MONGO_URI"] = "mongodb+srv://mealmate_user:TdJkLWwcc8DUIa1O@cluster0.6kr0juf.mongodb.net/mealmate?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)


#mongo client accessiblity
app.mongo = mongo

#blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(ingredient_bp)
app.register_blueprint(recipe_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/debug/ingredients')
def debug_ingredients():
    mongo = current_app.mongo
    all_ingredients = list(mongo.db.ingredients.find())
    for doc in all_ingredients:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string for display
    return {"ingredients": all_ingredients}

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

