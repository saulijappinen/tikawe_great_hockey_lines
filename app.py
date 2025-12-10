import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, flash

# standard libraries come to any venv(?) so random works!
from random import choice
from  secrets import token_hex

# import python modules from /
import db
import config # 
import items
import users 

# BEGIN APP
app = Flask(__name__)
app.secret_key = config.secret_key # for session

@app.context_processor #NOTE: this handles to templates but still need to use in app.py as well so config.INPUTLENGHTLIMITS below!
def inject_globals():
    return {'INPUT_LENGTH_LIMITS': config.INPUT_LENGTH_LIMITS}
 
# globals

## used in index
nhl_teams = ["Lightning ⚡️", "Panther 🐆", "Duck 🦆", "Penquin 🐧", "Leaf 🍁", "Shark 🦈", "Star ⭐️", "Devil 😈"]
input_random_team = choice(nhl_teams)

# pages
@app.route("/")
def index():
    items_all = items.get_all_items()
    return render_template("index.html", random_team=input_random_team, items_displayed=items_all)

# general / only check, no returns

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf(): 
    if "csrf_token" not in request.form: 
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]: # malicious field
        abort(403)

# lines/items stuff

@app.route("/item/<int:item_id>") 
def show_item(item_id):

    require_login()

    item = items.get_one_item(item_id)

    if not item: 
        abort(404) 

    rating = items.get_ratings(item_id)
    classes_for_item = items.get_classes_for_item(item_id)

    grouped_classes = {} # for printing on page
    
    for entry in classes_for_item:
        title = entry["title"]
        if title not in grouped_classes:
            grouped_classes[title] = []
        grouped_classes[title].append(entry["value"])

    return render_template("item_page.html", 
                           item_page=item, 
                           rating_page=rating,
                           classes_page=grouped_classes)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):

    require_login()

    item = items.get_one_item(item_id)

    if not item: 
        abort(404) 

    if item["user_id"] != session["user_id"]:
        abort(403) 

    all_classes = items.get_all_classes() 

    selected_classes = {}

    # Initialize with the title as key (my_class is already a string)
    for my_class in all_classes:
        selected_classes[my_class] = []

    # Append all values for each title
    for entry in items.get_classes_for_item(item_id): 
        title = entry["title"]
        if title in selected_classes:
            selected_classes[title].append(entry["value"])

    return render_template("item_edit.html", item_page=item, all_classes=all_classes, selected_classes=selected_classes)

@app.route("/delete_item/<int:item_id>", methods=["GET", "POST"])
def delete_item(item_id):

    require_login()

    item = items.get_one_item(item_id)

    if not item: 
        abort(404) 

    if item["user_id"] != session["user_id"]:
        abort(403) 

    if request.method == "GET":
        return render_template("item_delete.html", item=item)

    if request.method == "POST":
        check_csrf() 
        if "delete" in request.form:
            items.delete_item(item_id)
            flash("A line got deleted from database!", "success")
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
        
@app.route("/find_item")
def find_item():

    require_login()

    query = request.args.get("query")
    
    if query:
        search_results = items.find_items(query) 
    else: # to handle empty search / when coming to page
        query = ""
        search_results = []
    return render_template("item_find.html", query=query, results=search_results)

@app.route("/add_item") # just the page, create_item adds to data base
def add_item():

    require_login()

    possible_classes = items.get_all_classes()

    return render_template("item_add.html", classes=possible_classes)

@app.route("/create_item", methods=["POST"]) # item_add posts to this
def create_item():

    require_login()
    check_csrf()

    user_id = session["user_id"]
    
    input_linename = request.form["linename"]
    input_player_lw = request.form["player_lw"]
    input_player_c = request.form["player_c"]
    input_player_rw = request.form["player_rw"]

    if not input_linename or len(input_player_lw) > config.INPUT_LENGTH_LIMITS['item_input']:
        abort(403)
    if not input_player_lw or len(input_player_lw) > config.INPUT_LENGTH_LIMITS['item_input']:
        abort(403)
    if not input_player_c or len(input_player_c) > config.INPUT_LENGTH_LIMITS['item_input']:
        abort(403)
    if not input_player_rw or len(input_player_rw) > config.INPUT_LENGTH_LIMITS['item_input']:
        abort(403)
    
    # classes part
    all_classes = items.get_all_classes()

    input_classes = []

    for entry in request.form.getlist("category"): # go through 2 possible cats and append classes
        if entry:
            class_title, class_value = entry.split("_") # see html category value
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            input_classes.append((class_title, class_value))
    
    # only for checking!

    keys = {item[0] for item in input_classes} #   set, only unique!

    if 'league' not in keys or 'nationality' not in keys: 
        flash("Need to insert at least one league and nationality!", "error")
        return redirect("/add_item")

    # write to db AND return the id! not cool but works.. 
    item_id = items.add_item(input_linename, input_player_lw, input_player_c, input_player_rw, user_id, input_classes)

    return redirect("/item/" + str(item_id))

@app.route("/update_item", methods=["POST"]) 
def update_item():

    require_login()
    check_csrf()
   
    item_id = request.form["item_id"]  # item id from page hidden variable

    item = items.get_one_item(item_id) # need to do here also because content could be altered for another item (video 8), not just in edit/delete!

    if item["user_id"] != session["user_id"]:
        abort(403)

    user_id = session["user_id"]

    # main info
    input_linename = request.form["linename"]
    input_player_lw = request.form["player_lw"]
    input_player_c = request.form["player_c"]
    input_player_rw = request.form["player_rw"]

    if not input_linename or len(input_player_lw) > config.INPUT_LENGTH_LIMITS['item_input']:
        abort(403)
    if not input_player_lw or len(input_player_lw) > config.INPUT_LENGTH_LIMITS['item_input']:
        abort(403)
    if not input_player_c or len(input_player_c) > config.INPUT_LENGTH_LIMITS['item_input']:
        abort(403)
    if not input_player_rw or len(input_player_rw) > config.INPUT_LENGTH_LIMITS['item_input']:
        abort(403)

    # classes
    all_classes = items.get_all_classes()

    input_classes = []

    for entry in request.form.getlist("category"): # go through 2 possible cats and append classes
        if entry:
            class_title, class_value = entry.split("_") # see html category value
            # prevent html editing!
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            input_classes.append((class_title, class_value))

    # only for checking!
    
    keys = {item[0] for item in input_classes} #   set, only unique!

    if 'league' not in keys or 'nationality' not in keys: 
        flash("Need to insert at least one league and nationality!", "error")
        return redirect("/edit_item/" + str(item_id))

    items.update_item(input_linename, input_player_lw, input_player_c, input_player_rw, item_id, input_classes)

    return redirect("item/" + str(item_id))

@app.route("/create_rating", methods=["POST"]) 
def create_rating():

    require_login()
    check_csrf()

    input_rating = request.form["rating"]
    user_id = session["user_id"]
    item_id = request.form["item_id"]

    items.add_rating(item_id, user_id, input_rating)

    return redirect("item/" + str(item_id))



# user stuff ------

@app.route("/register") # this posts to /create, not login!!
def register():

    if "user_id" in session:
        flash("You can only register if you are not logged in!", "error")
        return redirect("/")

    return render_template("register.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("Inserted passwords not equal!", "error")
        return redirect("/register")

    try:
        users.create_user(username, password1) # hash created inside function
    except sqlite3.IntegrityError:
        flash("User already exists!", "error")
        return redirect("/register")
    
    flash(f"Congratulations {username}! Please login next.", "success")

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"]) 
def login():

    if request.method == "GET": 
        if "user_id" in session:
            flash("You are already logged in. Log out first to log in as another user.", "error")
            return redirect("/")
        else:
            return render_template("login.html", filled={})
         
    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password) # only returns if user exists
     
        if user_id: 
            # these are kept in memory for the whole session
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = token_hex(16) # one token for one sign in
            return redirect("/")
        else:
            flash("Wrong username or password!", "error")
            filled = {"username": username}
            return render_template("login.html", filled=filled)

@app.route("/logout")
def logout():
    if "user_id" in session: 
        del session["username"]
        del session["user_id"]
    return redirect("/")

@app.route("/user/<int:user_id>") 
def show_user(user_id):

    require_login()

    user_info = users.get_user_info(user_id)

    if not user_info: # function returns None if no user
        abort(404) 

    user_items = users.get_user_items(user_id)

    return render_template("user_page.html", user=user_info, items=user_items)