DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS tag;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    headimge TEXT NOT NULL
);

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dirname TEXT NOT NULL COLLATE NOCASE,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    tags TEXT COLLATE NOCASE,

    FOREIGN KEY (author_id) REFERENCES user(id)
);

CREATE TABLE tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    name TEXT NOT NULL,

    FOREIGN KEY (post_id) REFERENCES post(id)
);

INSERT INTO user (
    username, password, headimge
) VALUES (
    0, 0, "default.jpg"
);
INSERT INTO post (
    title, 
    body, 
    author_id, 
    dirname, 
    tags
) VALUES (
    "Welcome!", 
    "Welcome to the memory river!\nYou can write your diary there!",
    0, 
    "auto",
    ""
);
