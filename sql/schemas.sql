-- visit to site (index)
CREATE TABLE visits (
    id INTEGER PRIMARY KEY, -- id_visit!!
    visited_at TEXT
);

-- users and hashed pw
CREATE TABLE users (
    id INTEGER PRIMARY KEY, -- change to id_user!
    username TEXT UNIQUE,
    password_hash TEXT, 
    creation_time TEXT 
);


CREATE TABLE items (
    id INTEGER PRIMARY KEY, -- change to id_item!!
    linename TEXT UNIQUE, -- but only unique name
    player_lw TEXT, -- same player can be in multiple lines!
    player_c TEXT,
    player_rw TEXT,
    user_id INTEGER REFERENCES users,
    modification_time TEXT 
);

CREATE TABLE ratings (
    id INTEGER PRIMARY KEY, 
    item_id INTEGER REFERENCES items, 
    user_id INTEGER REFERENCES users,
    rating INTEGER, 
    rating_time TEXT 
);