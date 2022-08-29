import sqlite3
import random
import sys
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def read_from_db(dish_type):
    conn = get_db_connection()
    query = 'SELECT * FROM dishes WHERE dish_type=? AND cooked=0'
    dishes = conn.execute(query, [dish_type]).fetchall()
    conn.close()
    return dishes

def write_to_db(dish_name, dish_type):
    conn = get_db_connection()
    query = 'INSERT INTO dishes (dish_name, cooked, dish_type) VALUES (?, ?, ?)'
    conn.execute(query, (dish_name, 0, dish_type))
    return

def change_dish_status():
    return

@app.route('/')
def home():
    dishes = read_from_db('main')
    return render_template('home.html', dishes=dishes)

@app.route('/')
def confirm():
    change_dish_status()
    dishes = read_from_db('main')
    return render_template('home.html', dishes=dishes)

@app.route('/meal')
def pick_meal():
    dishes = read_from_db('main')
    meal_choice = random.randint(1, len(dishes))
    for k in dishes:
        if k['id'] == meal_choice:
            dish = k['dish_name']
    return render_template('pick.html', dish=dish)

@app.route('/add_dish')
def add_dish():
    return render_template('add_dish.html')

@app.route('/confirmation', methods=['POST'])
def confirmation():
    dish_name = request.form.get("dish_name")
    dish_type = request.form.get("dish_type")
    write_to_db(dish_name, dish_type)
    return render_template('confirmation.html', dish_name=dish_name)