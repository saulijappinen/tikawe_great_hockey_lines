from werkzeug.security import check_password_hash, generate_password_hash

import db_module

def get_user_info(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db_module.query(sql, [user_id])
    return result[0] if result else None

def get_user_items(user_id):
    sql = "SELECT id, linename FROM items WHERE user_id = ? ORDER BY id DESC"
    return db_module.query(sql, [user_id])
