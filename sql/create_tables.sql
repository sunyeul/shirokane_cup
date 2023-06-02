DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    display_name TEXT,
    hashed_password TEXT
);

.mode csv
.import data/users.csv users

DROP TABLE IF EXISTS competitions;

CREATE TABLE competitions(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    title TEXT,
    description TEXT
);

.mode csv
.import data/competitions.csv competitions

DROP TABLE IF EXISTS submissions;

CREATE TABLE submissions(
    id INTEGER PRIMARY KEY,
    competition_id INTEGER,
    user_id INTEGER,
    description TEXT,
    score FLOAT,
    upload_date TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),

    Foreign Key(competition_id) REFERENCES competitions(id),
    Foreign Key(user_id) REFERENCES users(id)
);
