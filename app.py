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

def change_dish_status():
    return

@app.route('/')
def home():
    dishes = get_data('main')
    return render_template('home.html', dishes=dishes)

@app.route('/')
def confirm():
    change_dish_status()
    dishes = get_data('main')
    return render_template('home.html', dishes=dishes)

@app.route('/meal')
def pick_meal():
    dishes = get_data('main')
    meal_choice = random.randint(1, len(dishes))
    for k in dishes:
        if k['id'] == meal_choice:
            dish = k['dish_name']
    return render_template('pick.html', dish=dish)