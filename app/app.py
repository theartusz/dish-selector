from random import sample
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
from mongoengine import connect, Document, StringField, ObjectIdField, BooleanField
import sys
import os
from pymongo import MongoClient


app = Flask(__name__)

# load env variables
load_dotenv()

class Config(object):
    # create secret for wtforms
    SECRET_KEY = os.getenv('SECRET_KEY')
# initialize config
app.config.from_object(Config)
# connect to database
conn_str = ('mongodb+srv://artur:'+os.getenv('MONGODB_KEY')+'@db-cluster.8eqt6lf.mongodb.net/dish-selector?retryWrites=true&w=majority')
connect(host=conn_str)
# Initialize the database

#client = MongoClient(conn_str)
#db = client['dish-selector']
#coll = db.dishes
# create db model
class Dish(Document):
#    __tablename__ = 'dishes'
    DISH_TYPES = ('main', 'salad')
    _id = ObjectIdField()
    dish_name = StringField(max_length=50, required=True)
    dish_type = StringField(max_length=50, required=True, choices=DISH_TYPES)
    cooked = BooleanField(default=False)
    meta = {'collection': 'dishes'}

    # create a string
    def __repr__(self):
        return '<dish name: %s, dish type: %s, cooked: %s>' % (self.dish_name, self.dish_type, self.cooked)

# create a form class
class NewDishForm(FlaskForm):
    dish_name = StringField(' Name of dish you want to add', validators=[DataRequired()])
    dish_type = StringField('Type of the dish', validators=[DataRequired()])
    submit = SubmitField("Submit")

def change_dish_status(dish_type):
    Dish.objects(dish_type=dish_type).update(cooked=False)
    return

@app.route('/', methods=['GET', 'POST'])
def home():
    dishes = Dish.objects(cooked=False)
    # reset dishes if all were cooked
    dish_types = ['main', 'salad']
    for dish_type in dish_types:
        if not Dish.objects(dish_type=dish_type, cooked=False).first():
            change_dish_status(dish_type)
    if request.method == 'POST':
        dish_type = request.form.get('name')
        return redirect(url_for('pick_meal', dish_type=dish_type))
    return render_template('home.html', dishes=dishes)

@app.route('/<dish_id>')
def confirm(dish_id):
    Dish.objects(_id = dish_id).update_one(cooked=True)
    return redirect(url_for('home'))

@app.route('/pick_meal/<string:dish_type>', methods=['GET', 'POST'])
def pick_meal(dish_type):
    #pick random dish which was not cooked yet
    dish = list(Dish.objects(dish_type = dish_type, cooked = False).aggregate([{ "$sample": { "size": 1 } }]))[0]
    return render_template('pick_meal.html', dish=dish, dish_type=dish_type)

@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    dish_name, dish_type = None, None
    form = NewDishForm()
    print(form.dish_name, file=sys.stdout)
    # validate form
    if form.validate_on_submit():
        dish_name = form.dish_name.data
        dish_type = form.dish_type.data
        form.dish_name.data, form.dish_type.data = '', ''
        Dish(dish_name=dish_name, dish_type=dish_type, cooked=False).save()
        return redirect('/add_dish')
    else:
        return render_template('add_dish.html', dish_name=dish_name, dish_type=dish_type, form=form)