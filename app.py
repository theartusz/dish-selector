import sqlite3
import random
import sys
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_data(dish_type):
    conn = get_db_connection()
    query = 'SELECT * FROM dishes WHERE dish_type=? AND cooked=0'
    dishes = conn.execute(query, [dish_type]).fetchall()
    conn.close()
    return dishes

@app.route('/', methods=['GET', 'POST'])
def index():
    dishes = get_data('main')

    if request.method == 'POST':
        if request.form.get('pick') == 'Pick random dish':
            return redirect("meal")
    return render_template('index.html', dishes=dishes)

@app.route('/meal')
def pick_meal():
    dishes = get_data('main')
    meal_choice = random.randint(1, len(dishes))
    for k in dishes:
        print(k['id'], file=sys.stderr)
        print('Meal choice: '+str(meal_choice), file=sys.stdout)
        if k['id'] == meal_choice:
            dish = k['dish_name']
    return render_template('pick.html', dish=dish)