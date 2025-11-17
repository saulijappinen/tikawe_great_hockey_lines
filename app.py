import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort

from werkzeug.security import generate_password_hash, check_password_hash

# standard libraries come to any venv(?) so random works!
from random import choice

# import python modules from /
import db_module
import config # 
import items


# BEGIN APP
app = Flask(__name__)
app.secret_key = config.secret_key # for session
 
# globals

## used in index
nhl_teams = ["Lightning ⚡️", "Panther 🐆", "Duck 🦆", "Penquin 🐧"]
input_random_team = choice(nhl_teams)

# pages
@app.route("/")
def index():
    items_all = items.get_all_items()
    return render_template("index.html", random_team=input_random_team, items_displayed=items_all)



# lines/items stuff

@app.route("/item/<int:item_id>") # one page for every line in db
def show_item(item_id):
    item = items.get_one_item(item_id)
    return render_template("item_page.html", item_page=item)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    item = items.get_one_item(item_id)

    if item["user_id"] != session["user_id"]:
        abort(403) # https://en.wikipedia.org/wiki/HTTP_403

    return render_template("item_edit.html", item_page=item)

@app.route("/delete_item/<int:item_id>", methods=["GET", "POST"])
def delete_item(item_id):

    item = items.get_one_item(item_id)

    if item["user_id"] != session["user_id"]:
        abort(403) # https://en.wikipedia.org/wiki/HTTP_403

    if request.method == "GET":
        return render_template("item_delete.html", item=item)

    if request.method == "POST":
        if "delete" in request.form:
            items.delete_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
        
@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        print("searching database")
        search_results = items.find_items(query) # can be many lines!
    else: # to handle empty search / when coming to page
        query = ""
        search_results = []
    return render_template("item_find.html", query=query, results=search_results)

@app.route("/add_line")
def add_line():
    return render_template("add_line.html")

@app.route("/create_line", methods=["POST"]) # add_line posts to this
def create_item():
    # user info
    user_id = session["user_id"]
    # main info
    input_linename = request.form["linename"]
    input_player_lw = request.form["player_lw"]
    input_player_c = request.form["player_c"]
    input_player_rw = request.form["player_rw"]
    # attributes
    # input_decade = request.form["decade"]
    # input_league = request.form["league"]
    # input_nationality = request.form.getlist("nationality")

    # write to db
    items.add_item(input_linename, input_player_lw, input_player_c, input_player_rw, user_id)

    # try:
    #     sql = "INSERT INTO items (linename, player_lw, player_c, player_rw, user_id) VALUES (?, ?, ?, ?, ?)"
    #     db_module.execute(sql, [input_linename, input_player_lw, input_player_c, input_player_rw, user_id]) 
    # except sqlite3.IntegrityError:
    #     return "ERROR: line addition did not succeed!" 
    
    # ret to main page
    #return redirect("/")

    # ret to result page
    return render_template("result.html", 
                           linename=input_linename,
                           player_lw = input_player_lw, 
                           player_c = input_player_c, 
                           player_rw = input_player_rw
                           #decade=input_decade, nationalities = input_nationality,league = input_league
                           )

@app.route("/update_item", methods=["POST"]) # add_line posts to this
def update_item():
    # item id from page hidden variable
    item_id = request.form["item_id"]

    item = items.get_item(item_id) # need to do here also because content could be altered for another item (video 8), not just in edit/delete!

    if item["user_id"] != session["user_id"]:
        abort(403)

    # user info
    user_id = session["user_id"]
    # main info
    input_linename = request.form["linename"]
    input_player_lw = request.form["player_lw"]
    input_player_c = request.form["player_c"]
    input_player_rw = request.form["player_rw"]
    # attributes
    # input_decade = request.form["decade"]
    # input_league = request.form["league"]
    # input_nationality = request.form.getlist("nationality")

    # write to db / user_id and line id not altered!!
    items.update_item(input_linename, input_player_lw, input_player_c, input_player_rw, item_id)

    # ret to item page
    return redirect("item/" + str(item_id))


# user stuff

@app.route("/register") # this posts to /create, not login!!
def register():
    return render_template("register.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: inserted passwords not equal!"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db_module.execute(sql, [username, password_hash]) 
    except sqlite3.IntegrityError:
        return "ERROR: user already exists!"

    return f'''
        <h2>Congratulations {username}!</h2>
        <p>
        You are now a member of our community!<br>
        Please, <a href="/login">log in</a> next.
        </p>
        '''

@app.route("/login", methods=["GET", "POST"]) # both methods!
def login():
    if request.method == "GET": 
        return render_template("login.html")
         
    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]
   
        sql = "SELECT id, password_hash FROM users WHERE username = ?" # select also id because needed in other places
        result = db_module.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]
     
        if check_password_hash(password_hash, password):
            # these are kept in memory for the whole session
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return 'Error: wrong username or password! Please try <a href="/login">logging in</a> again.'

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")