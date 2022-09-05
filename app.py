from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from config import Config

app = Flask(__name__)
# initialize config
app.config.from_object(Config)
# Initialize the database
db = SQLAlchemy(app)

# create db model
class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(50), nullable=False)
    dish_type = db.Column(db.String(20), nullable=False)
    cooked = db.Column(db.Boolean, nullable=False)

    # create a string
    def __repr__(self):
        return '<dish name: %s, dish type: %s, cooked: %s>' % (self.dish_name, self.dish_type, self.cooked)

# create a form class
class NewDishForm(FlaskForm):
    dish_name = StringField(' Name of dish you want to add', validators=[DataRequired()])
    dish_type = StringField('Type of the dish', validators=[DataRequired()])
    submit = SubmitField("Submit")

def change_dish_status(dish_type):
    db.session.query(Dish).filter(Dish.dish_type == dish_type).update({'cooked': 0})
    db.session.commit()
    return

@app.route('/', methods=['GET', 'POST'])
def home():
    dishes = db.session.query(Dish).filter(Dish.cooked == 0)
    # reset dishes if all were cooked
    dish_types = ['main', 'salad']
    for dish_type in dish_types:
        if not dishes.filter(Dish.dish_type == dish_type).first():
            change_dish_status(dish_type)

    if request.method == 'POST':
        dish_type = request.form.get('name')
        return redirect(url_for('pick_meal', dish_type=dish_type))
    return render_template('home.html', dishes=dishes)

@app.route('/<dish_id>')
def confirm(dish_id):
    db.session.query(Dish).filter(Dish.id == dish_id).update({'cooked': 1})
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/pick_meal/<string:dish_type>', methods=['GET', 'POST'])
def pick_meal(dish_type):
    #pick random dish which was not cooked yet
    dish = db.session.query(Dish).filter(Dish.dish_type == dish_type, Dish.cooked == 0).order_by(func.random()).first()
    return render_template('pick_meal.html', dish=dish, dish_type=dish_type)

@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    dish_name, dish_type = None, None
    form = NewDishForm()
    # validate form
    if form.validate_on_submit():
        dish_name = form.dish_name.data
        dish_type = form.dish_type.data
        form.dish_name.data, form.dish_type.data = '', ''
        new_dish = Dish(dish_name=dish_name, dish_type=dish_type, cooked=0)

        #push to database
        db.session.add(new_dish)
        db.session.commit()
        return redirect('/add_dish')
    else:
        return render_template('add_dish.html', dish_name=dish_name, dish_type=dish_type, form=form)