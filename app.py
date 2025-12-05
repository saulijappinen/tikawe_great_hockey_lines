import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, flash

# standard libraries come to any venv(?) so random works!
from random import choice
from  secrets import token_hex

# import python modules from /
import db_module
import config # 
import items
import users 

# BEGIN APP
app = Flask(__name__)
app.secret_key = config.secret_key # for session
 
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
    if "csrf_token" not in request.form: # form does not return token at all
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]: # malicious field
        abort(403)

# lines/items stuff

@app.route("/item/<int:item_id>") # one page for every line in db
def show_item(item_id):

    require_login()

    item = items.get_one_item(item_id)

    if not item: 
        abort(404) # https://en.wikipedia.org/wiki/HTTP_404

    rating = items.get_ratings(item_id)
    classes_for_item = items.get_classes_for_item(item_id)

    grouped_classes = {} # for printing on page
    
    for entry in classes_for_item:
        title = entry["title"]
        if title not in grouped_classes:
            grouped_classes[title] = []
        grouped_classes[title].append(entry["value"])

    print(grouped_classes)

    return render_template("item_page.html", 
                           item_page=item, 
                           rating_page=rating,
                           classes_page=grouped_classes)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):

    require_login()

    item = items.get_one_item(item_id)

    if not item: # function returns None if no ID
        abort(404) # https://en.wikipedia.org/wiki/HTTP_404

    if item["user_id"] != session["user_id"]:
        abort(403) # https://en.wikipedia.org/wiki/HTTP_403

    all_classes = items.get_all_classes() # all possible

    selected_classes = {}

    # Initialize with the title as key (my_class is already a string)
    for my_class in all_classes:
        selected_classes[my_class] = []

    # Append all values for each title
    for entry in items.get_classes_for_item(item_id): 
        title = entry["title"]
        if title in selected_classes:
            selected_classes[title].append(entry["value"])

    print("selected classes are: ", selected_classes)

    return render_template("item_edit.html", item_page=item, all_classes=all_classes, selected_classes=selected_classes)

@app.route("/delete_item/<int:item_id>", methods=["GET", "POST"])
def delete_item(item_id):

    require_login()

    item = items.get_one_item(item_id)

    if not item: # function returns None if no ID
        abort(404) # https://en.wikipedia.org/wiki/HTTP_404

    if item["user_id"] != session["user_id"]:
        abort(403) # https://en.wikipedia.org/wiki/HTTP_403

    if request.method == "GET":
        return render_template("item_delete.html", item=item)

    if request.method == "POST":
        check_csrf() # only done when posting
        if "delete" in request.form:
            items.delete_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
        
@app.route("/find_item")
def find_item():

    require_login()

    query = request.args.get("query")
    
    if query:
        print("searching database")
        search_results = items.find_items(query) # can be many lines!
    else: # to handle empty search / when coming to page
        query = ""
        search_results = []
    return render_template("item_find.html", query=query, results=search_results)

@app.route("/add_line") # just the page, create_line adds to data base
def add_line():

    require_login()

    print(items.get_all_classes())

    possible_classes = items.get_all_classes()

    return render_template("add_line.html", classes=possible_classes)

@app.route("/create_line", methods=["POST"]) # add_line posts to this
def create_item():

    require_login()
    check_csrf()

    user_id = session["user_id"]
    
    input_linename = request.form["linename"]
    input_player_lw = request.form["player_lw"]
    input_player_c = request.form["player_c"]
    input_player_rw = request.form["player_rw"]

    if not input_linename or len(input_linename) > 100:
        abort(403)
    if not input_player_lw or len(input_player_lw) > 100:
        abort(403)
    if not input_player_c or len(input_player_c) > 100:
        abort(403)
    if not input_player_rw or len(input_player_rw) > 100:
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
            print(class_title, class_value)
          
    if len(input_classes) < 2: #TODO: check both class_titles separately
        print("tänne mentiin")
        flash("ERROR: Need to insert at least one league and nationality!")
        return redirect("/add_line")

    # write to db AND return the id! not cool but works.. 
    item_id = items.add_item(input_linename, input_player_lw, input_player_c, input_player_rw, user_id, input_classes)

    print("item id is", item_id)

    return redirect("/item/" + str(item_id))

    # ret to result page
    # return render_template("result.html", 
    #                        linename=input_linename,
    #                        player_lw = input_player_lw, 
    #                        player_c = input_player_c, 
    #                        player_rw = input_player_rw
    #                        #decade=input_decade, nationalities = input_nationality,league = input_league
    #                        )

@app.route("/update_item", methods=["POST"]) # add_line posts to this
def update_item():

    require_login()
    check_csrf()

    # item id from page hidden variable
    item_id = request.form["item_id"]

    item = items.get_one_item(item_id) # need to do here also because content could be altered for another item (video 8), not just in edit/delete!

    if item["user_id"] != session["user_id"]:
        abort(403)

    # user info
    user_id = session["user_id"]
    # main info
    input_linename = request.form["linename"]
    input_player_lw = request.form["player_lw"]
    input_player_c = request.form["player_c"]
    input_player_rw = request.form["player_rw"]

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
            print(class_title, class_value)

    # write to db / user_id and line id not altered!!
    items.update_item(input_linename, input_player_lw, input_player_c, input_player_rw, item_id, input_classes)

    # ret to item page
    return redirect("item/" + str(item_id))

@app.route("/create_rating", methods=["POST"]) 
def create_rating():

    require_login()
    check_csrf()

    input_rating = request.form["rating"]
    user_id = session["user_id"]
    item_id = request.form["item_id"]

    # write to db
    items.add_rating(item_id, user_id, input_rating)

    return redirect("item/" + str(item_id))



# user stuff ------

@app.route("/register") # this posts to /create, not login!!
def register():
    return render_template("register.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("ERROR: inserted passwords not equal!")
        return redirect("/register")

    try:
        users.create_user(username, password1) # hash created inside function
    except sqlite3.IntegrityError:
        flash("ERROR: user already exists!")
        return redirect("/register")
    
    flash(f"Congratulations {username}! Please login next.")

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"]) # both methods!
def login():
    if request.method == "GET": 
        return render_template("login.html", filled={})
         
    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password) # only returns if user exists
     
        if user_id: # if exists = check_login returns id 
            # these are kept in memory for the whole session
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = token_hex(16) # one token for one sign in
            print(f"session token is {session["csrf_token"]}")
            return redirect("/")
        else:
            flash("Error: wrong username or password!")
            filled = {"username": username}
            return render_template("login.html", filled=filled)

@app.route("/logout")
def logout():
    if "user_id" in session: # when logged in
        del session["username"]
        del session["user_id"]
    return redirect("/")

@app.route("/user/<int:user_id>") 
def show_user(user_id):

    user_info = users.get_user_info(user_id)

    if not user_info: # function returns None if no user
        abort(404) # https://en.wikipedia.org/wiki/HTTP_404

    user_items = users.get_user_items(user_id)

    return render_template("user_page.html", user=user_info, items=user_items)