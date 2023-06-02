DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT,
    hashed_password TEXT
);

.mode csv
.import data/users.csv users

DROP TABLE IF EXISTS competitions;

CREATE TABLE competitions(
    id INTEGER PRIMARY KEY,
    title TEXT,
    subtitle TEXT,
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
