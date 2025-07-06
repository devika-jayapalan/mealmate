from flask import Flask, render_template
from flask_pymongo import PyMongo
from routes.auth_routes import auth_bp
from routes.ingredient_routes import ingredient_bp
#from routes.recipe_routes import recipe_bp

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mealplanner"
mongo = PyMongo(app)

#mongo client accessiblity
app.mongo = mongo

#blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(ingredient_bp)
#app.register_blueprint(recipe_bp)

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

