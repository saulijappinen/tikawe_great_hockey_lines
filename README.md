# tikawe_great_hockey_lines

My course project for course <a href="https://hy-tikawe.github.io/materiaali/">Tietokannat ja web-ohjelmointi</a> (University of Helsinki).

## Functionalities of the app

The main idea is to add and browse hockey forward lines.

### Changelog

see `NEWS.md`


### Current functionalities

* a user can
  * create a user account to use the app
  * log in (and out) of the app
  * add lines and modify or delete the ones he/she has his/herself added
  * see all the lines added
  * search the lines based on a search word
    * search includes line name and player names
  * add reviews of the lines added (from 1 to 5)
  * browse a user page that shows the lines added by the user (at least) and other basic info of the user

* information included of the lines
  * line and player names (main information)
  * additional attributes (classes)
    * nationalities of the players
    * what leagues was that line in
  * rating (1 to 5) of the line (based on reviews)


## How to use

Make sure python is installed and then create and activate virtual environment with the following

```
$ python3 -m venv venv
$ source venv/bin/activate
```

install `flask` library and dependencies to your virtual environment

```
$ pip install flask
```

Create sqlite database and initialize content from .sql files (and see the tables included)

```
# create database and init classes
$ sqlite3 database.db < sql/schemas.sql
$ sqlite3 database.db < sql/init_classes.sql

# check content (not required)
$ sqlite3 database.db # open connection to database
$ sqlite3 .tables # see tables
$ sqlite3 .quit # close db
```

Run the app

```
$ flask run
```

*Hints*

You can find possible lines to be added for example in:

<https://thehockeywriters.com/top-10-nhl-lines/>

or add the famous Tupu-Hupu-Lupu line from '95!



------

## Repository structure

`/`

**modules**

* config.py
* app.py
* db.py: database functions
* items.py: functions related to items (lines)
* users.py: functions related to users

**Documentation files**

* news.md: release version notes

`templates`

* html pages for render_template function

`sql`

* sql files for creating tables to database

`pylint`

* pylint report for module files and own comments

## Additional information

* built on the following
  * Python version 3.13.7
  * sqlite3 version 3.37.0
