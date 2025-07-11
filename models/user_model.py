def get_user_by_email(mongo, email):
    return mongo.db.users.find_one({"email": email})

def create_user(mongo, name, email):
    return mongo.db.users.insert_one({
        "name": name,
        "email": email
    }).inserted_id
