DROP TABLE IF EXISTS posts;

CREATE TABLE dishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dish_name TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cooked  BOOLEAN NOT NULL,
    dish_type TEXT NOT NULL
);