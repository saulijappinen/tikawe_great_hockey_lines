-- visit to site (index)
CREATE TABLE visits (
    id INTEGER PRIMARY KEY, 
    visited_at TEXT
);

-- users and hashed pw
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);


CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    linename TEXT UNIQUE, -- but only unique name
    player_lw TEXT, -- same player can be in multiple lines!
    player_c TEXT,
    player_rw TEXT,
    user_id INTEGER REFERENCES users
);