DROP TABLE IF EXISTS signin;

CREATE TABLE signin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL
);