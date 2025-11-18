from werkzeug.security import check_password_hash, generate_password_hash

import db_module

def get_user_info(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db_module.query(sql, [user_id])
    return result[0] if result else None

def get_user_items(user_id):
    sql = "SELECT id, linename FROM items WHERE user_id = ? ORDER BY id DESC"
    return db_module.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db_module.execute(sql, [username, password_hash])
    print("user created")

def check_login(username, password): # get_user_name_when_logging_in
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    res = db_module.query(sql, [username])
    if not res: # fail 1: no user 
        return None
    
    user_id = res[0]["id"]
    password_hash = res[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None # fail 2: password does not match