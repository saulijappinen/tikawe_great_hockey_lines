-- users and hashed pw
CREATE TABLE users (
    id INTEGER PRIMARY KEY, 
    username TEXT UNIQUE,
    password_hash TEXT, 
    creation_time TEXT 
);


CREATE TABLE items (
    id INTEGER PRIMARY KEY, 
    linename TEXT UNIQUE, 
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

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    title TEXT,
    value TEXT
);