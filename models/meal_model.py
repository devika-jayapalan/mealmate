from datetime import datetime, timedelta

def log_meal(mongo, user_id, day, meal_type, recipe_name):
    week_number = datetime.utcnow().isocalendar()[1]
    mongo.db.mealplans.insert_one({
        "user_id": user_id,
        "week_number": week_number,
        "meals": [{
            "day": day,
            "meal_type": meal_type,
            "recipe_name": recipe_name
        }]
    })

def get_meals_this_week(mongo, user_id):
    week_number = datetime.utcnow().isocalendar()[1]
    return list(mongo.db.mealplans.find({
        "user_id": user_id,
        "week_number": week_number
    }))
