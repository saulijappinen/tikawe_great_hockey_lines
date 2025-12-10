from datetime import datetime

import db_module

# for adding lines AND CLASSES!
def add_item(linename, player_lw, player_c, player_rw, user_id, classes):

    # line info to items
    curtime = datetime.now().replace(microsecond=0) # generated, not set when calling the function!
    sql = "INSERT INTO items (linename, player_lw, player_c, player_rw, user_id, modification_time) VALUES (?, ?, ?, ?, ?, ?)"
    db_module.execute(sql, [linename, player_lw, player_c, player_rw, user_id, curtime]) 
    print(f"Line {linename} added!") # for dev

    # classes of the line to classes
    item_id = db_module.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db_module.execute(sql, [item_id, class_title, class_value])

    return item_id # this so that redirect after adding works!!

# get functions 
def get_all_items(): # for displaying all

    return db_module.query(
        """
        SELECT i.id, 
        i.linename, 
        i.player_lw, 
        i.player_c, 
        i.player_rw, 
        i.user_id, 
        i.modification_time,
        u.username  
        
        FROM ITEMS as i
        
        LEFT JOIN USERS as u
            on i.user_id = u.id

        ORDER BY i.ID DESC
        """
        ) 


def get_one_item(item_id): # for displaying one
    print("running get_one_item() function")
    sql = """
    SELECT i.id 
    , i.linename 
    , i.player_lw 
    , i.player_c 
    , i.player_rw
    , i.user_id
    , i.modification_time  
    , u.username

    FROM ITEMS as i 
    
    LEFT JOIN USERS as u
        on i.user_id = u.id
    
    WHERE i.id =  ?
    """

    res = db_module.query(sql, [item_id]) # extra step so that none is option

    return res[0] if res else None

# altering items functions ----

def update_item(linename, player_lw, player_c, player_rw, item_id, classes):
    curtime = datetime.now().replace(microsecond=0) # generated, not set when calling the function!
    sql = """UPDATE items SET linename = ?,
                              player_lw = ?,
                              player_c = ?,
                              player_rw = ?,
                              modification_time = ?
                          WHERE id = ?"""
    db_module.execute(sql, [linename, player_lw, player_c, player_rw, curtime, item_id])
    print("update_item() executed")

    # CLASSES PART

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db_module.execute(sql, [item_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db_module.execute(sql, [item_id, class_title, class_value])

def delete_item(item_id):

    # FIRST NEED TO DELETE REFERENCES!!

    sql = "DELETE FROM ratings WHERE item_id = ?"
    db_module.execute(sql, [item_id])

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db_module.execute(sql, [item_id])

    sql = "DELETE FROM items WHERE id = ?"
    db_module.execute(sql, [item_id])

    print(f"{item_id} got deleted.")

def find_items(query):
    query_wildcards = f"%{query}%" # wildcards possible
    query_wildcards = query_wildcards.lower() # and make lowercase

    sql = """SELECT 
            i.id, 
            i.linename, 
            i.user_id,
            i.modification_time, 
            u.username
            
            FROM items as i 
            
            LEFT JOIN USERS as u
                on i.user_id = u.id

             WHERE lower(i.linename) LIKE ?
             or lower(i.player_lw) LIKE ?
             or lower(i.player_c) LIKE ?
             or lower(i.player_rw) LIKE ?
             ORDER BY i.id DESC"""
    
    return db_module.query(sql, [query_wildcards, query_wildcards, query_wildcards, query_wildcards])

# RATINGS

def add_rating(item_id, user_id, rating):
    curtime = datetime.now().replace(microsecond=0) # generated, not set when calling the function!
    sql = "INSERT INTO ratings (item_id, user_id, rating, rating_time) VALUES (?, ?, ?, ?)"
    db_module.execute(sql, [item_id, user_id, rating, curtime]) 
    print(f"Rating added to item {item_id}!") 

def get_ratings(item_id):    
    sql = """
    SELECT r.id
    , r.item_id  
    , r.user_id 
    , r.rating 
    , r.rating_time 
    , u.username

    FROM ratings as r 
    
    LEFT JOIN USERS as u
        on r.user_id = u.id
    
    WHERE r.item_id =  ? -- item-id, not rating id!
    ORDER BY r.id DESC
    """ 
    return db_module.query(sql, [item_id])

# CLASSES

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db_module.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_classes_for_item(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db_module.query(sql, [item_id])