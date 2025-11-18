# tikawe_great_hockey_lines

My course project for course `hy-tikawe`: hockey lines app - share your favorite hockey lines!

## Functionalities of the app

The main idea is to add and browse hockey forward lines. 

**The aim is to include the following functionalities**

* a user can 
  * create a user account to use the app 
  * log in (and out) of the app
  * add lines and modify or delete the ones he/she has his/herself added
  * see all the lines added
  * search the lines based on a search word (at least) and a attribute added to the lines (nationality, decade etc.)
  * add reviews of the lines added (from 1 to 5 pucks/sticks)
  * browse a user page that shows the lines added by the user (at least) and times when the user has logged in 
    * if time allows, also shows the ratings given to the lines added by the user 


* information included of the lines (at least the following)
  * line and player names (main information)
  * additional attributes
    * nationalities of the players
    * which decade the line was at its prime
    * what league was that line in
  * rating (1 to 5) of the line (based on reviews)


**Available features in the current release version (2.0), see `NEWS.md`**


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

Create sqlite database from schemas file (and see the tables included)

```
$ sqlite3 database.db < sql/schemas.sql
$ sqlite3 .tables 
$ sqlite3 .quit
```

Run the app

```
$ flask run
```

You can find possible lines to be added for example in: 

<https://thehockeywriters.com/top-10-nhl-lines/>


Additional information

* built on the following
  * Python 3.13.7 



------

## Repository structure

(in progress)

`/`

* config.py 
* app.py 
* db_module.py
* items.py: functions related to items (lines)
* users.py: functions related to users 

Documentation files: 

* news.md: release version notes 
* log.md: own notes on what has been done / notes to future self

`templates`

* html pages for render_template function
  
`sql`

* sql files for creating tables to database

## Other info

TBA