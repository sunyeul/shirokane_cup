DROP TABLE IF EXISTS user;

CREATE TABLE user(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    hashed_password TEXT
);

.mode csv
.import data/user.csv user