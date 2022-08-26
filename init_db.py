import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO dishes (dish_name, cooked, dish_type) VALUES (?, ?, ?)",
            ('Stryki', 0, 'main')
            )

cur.execute("INSERT INTO dishes (dish_name, cooked, dish_type) VALUES (?, ?, ?)",
            ('Pizza', 0, 'main')
            )

connection.commit()
connection.close()