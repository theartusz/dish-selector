from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId as OId

app = Flask(__name__)

# load env variables
load_dotenv()
class Config(object):
    # create secret for wtforms
    SECRET_KEY = os.getenv('SECRET_KEY')
# initialize config
app.config.from_object(Config)
# connect to database
conn_str = ('mongodb+srv://'+os.getenv('MONGODB_USER')+':'+os.getenv('MONGODB_KEY')+'@db-cluster.8eqt6lf.mongodb.net/dish-selector?retryWrites=true&w=majority')
client = MongoClient(conn_str)
db = client['dish-selector']
coll = db['dishes']

# create a form class
class NewDishForm(FlaskForm):
    dish_name = StringField(' Name of dish you want to add', validators=[DataRequired()])
    dish_type = StringField('Type of the dish', validators=[DataRequired()])
    submit = SubmitField("Submit")

def change_dish_status(dish_type):
    coll.update_many({'dish_type': dish_type}, {'$set': {'cooked': False}})
    return

@app.route('/', methods=['GET', 'POST'])
def home():
    dishes = coll.find({'cooked': False})
    # reset dishes if all were cooked
    dish_types = ['main', 'salad']
    for dish_type in dish_types:
        if not coll.find_one({'$and':[{'cooked': False}, {'dish_type': dish_type}]}):
            change_dish_status(dish_type)
    if request.method == 'POST':
        dish_type = request.form.get('name')
        return redirect(url_for('pick_meal', dish_type=dish_type))
    return render_template('home.html', dishes=dishes)

@app.route('/pick_meal/<string:dish_type>', methods=['GET', 'POST'])
def pick_meal(dish_type):
    dish = list(coll.aggregate([
        {'$match':{
            'cooked': False,
            'dish_type': dish_type}},
        { '$sample':{
            'size': 1 } }]))[0]
    return render_template('pick_meal.html', dish=dish, dish_type=dish_type)

@app.route('/<dish_id>')
def confirm(dish_id):
    coll.update_one({'_id': OId(dish_id)}, {'$set':{'cooked': True}})
    return redirect(url_for('home'))

@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    dish_name, dish_type = None, None
    form = NewDishForm()
    # validate form
    if form.validate_on_submit():
        dish_name = form.dish_name.data
        dish_type = form.dish_type.data
        form.dish_name.data, form.dish_type.data = '', ''
        coll.insert_one({'dish_name': dish_name, 'dish_type': dish_type, 'cooked': False})
        flash('Your dish '+dish_name+' was added!')
        return redirect('/add_dish')
    else:
        return render_template('add_dish.html', dish_name=dish_name, dish_type=dish_type, form=form)

if __name__ == "__main__":
    app.run(debug=False, port=5000)