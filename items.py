import db_module

# for adding lines 
def add_item(linename, player_lw, player_c, player_rw, user_id):
    sql = "INSERT INTO items (linename, player_lw, player_c, player_rw, user_id) VALUES (?, ?, ?, ?, ?)"
    db_module.execute(sql, [linename, player_lw, player_c, player_rw, user_id]) 
    print(f"Line {linename} added!") # for dev
