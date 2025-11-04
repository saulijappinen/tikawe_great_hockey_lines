import db_module

# for adding lines 
def add_item(linename, player_lw, player_c, player_rw, user_id):
    sql = "INSERT INTO items (linename, player_lw, player_c, player_rw, user_id) VALUES (?, ?, ?, ?, ?)"
    db_module.execute(sql, [linename, player_lw, player_c, player_rw, user_id]) 
    print(f"Line {linename} added!") # for dev

# get functions 
def get_all_items(): # for displaying all
    print("running get_all_items() function")
    # sql = """SELECT items.id, items.title, users.id user_id, users.username,
    #                 COUNT(bids.id) bid_count
    #          FROM items JOIN users ON items.user_id = users.id
    #                     LEFT JOIN bids ON items.id = bids.item_id
    #          GROUP BY items.id
    #          ORDER BY items.id DESC"""

    return db_module.query("SELECT * FROM ITEMS ORDER BY ID DESC") # in descending order


def get_one_item(item_id): # for displaying one
    print("running get_one_item() function")
    sql = """SELECT i.*, u.username
    FROM ITEMS as i 
    LEFT JOIN USERS as u
        on i.user_id = u.id
    WHERE i.id =  ?"""
    return db_module.query(sql, [item_id])[0]

# altering items functions ----

def update_item(linename, player_lw, player_c, player_rw, item_id):
    print("update_item() executed")
    sql = """UPDATE items SET linename = ?,
                              player_lw = ?,
                              player_c = ?,
                              player_rw = ?
                          WHERE id = ?"""
    db_module.execute(sql, [linename, player_lw, player_c, player_rw, item_id])

    # sql = "DELETE FROM item_classes WHERE item_id = ?"
    # db.execute(sql, [item_id])

    # sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    # for class_title, class_value in classes:
    #     db.execute(sql, [item_id, class_title, class_value])
