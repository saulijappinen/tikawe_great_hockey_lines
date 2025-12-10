from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

import db

def get_user_info(user_id):
    sql = "SELECT id, username, creation_time FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_user_items(user_id):
    sql = "SELECT id, linename, modification_time FROM items WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    curtime = datetime.now().replace(microsecond=0)
    sql = "INSERT INTO users (username, password_hash, creation_time) VALUES (?, ?, ?)"
    db.execute(sql, [username, password_hash, curtime])
    #print("user created")

def check_login(username, password): # get_user_name_when_logging_in
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    res = db.query(sql, [username])

    if not res: # fail 1: no user
        return None

    user_id = res[0]["id"]
    password_hash = res[0]["password_hash"]

    if check_password_hash(password_hash, password):
        return user_id

    return None # fail 2: password does not match
