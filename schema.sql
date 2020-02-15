DROP TABLE IF EXISTS user; /* if tables already exist, delete them */
DROP TABLE IF EXISTS post;

CREATE TABLE user (                      /*create user table with id username and password*/
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEST NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
