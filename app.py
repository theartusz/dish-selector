import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_data(dish_type):
    conn = get_db_connection()
    query = 'SELECT * FROM dishes WHERE dish_type = "main"'
    dishes = conn.execute(query).fetchall()
    conn.close()
    return dishes

def pick_meal(dish_type):
    dishes = get_data(dish_type)
    return

@app.route('/', methods=['GET', 'POST'])
def index():
    dishes = get_data('main')

    if request.method == 'POST':
        if request.form.get('pick') == 'Pick random dish':
            pass
    return render_template('index.html', dishes=dishes)