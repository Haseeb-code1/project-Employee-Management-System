from app.utils.db import fetch_one

def login(username, password):
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    user = fetch_one(query, (username, password))
    return user
