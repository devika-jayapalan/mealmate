from datetime import datetime

def save_ingredients(mongo, user_id, ingredients):
    mongo.db.ingredients.delete_many({"user_id": user_id})
    for item in ingredients:
        mongo.db.ingredients.insert_one({
            "user_id": user_id,
            "ingredient": item,
            "submitted_at": datetime.utcnow()
        })

def get_ingredients(mongo, user_id):
    return [doc["ingredient"] for doc in mongo.db.ingredients.find({"user_id": user_id})]
    

