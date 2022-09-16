from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from bson.objectid import ObjectId as ObId
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
import os

app = Flask(__name__)

# load env variables
load_dotenv()

# load secrets from azure key vault
keyVaultName = os.getenv("KEY_VAULT_NAME")
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = ManagedIdentityCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

kv_secret_key = client.get_secret(os.getenv('AZURE_KV_SECRET_KEY'))
kv_mongodb_key = client.get_secret(os.getenv('AZURE_KV_MONGODB_KEY'))

# create Flask Config object
class Config(object):
    # create secret for wtforms
    SECRET_KEY = kv_secret_key.value
# initialize config
app.config.from_object(Config)

# connect to database
conn_str = ('mongodb+srv://'+os.getenv('MONGODB_USER')+':'+kv_mongodb_key.value+'@db-cluster.8eqt6lf.mongodb.net/dish-selector?retryWrites=true&w=majority')
client = MongoClient(conn_str)
db = client['dish-selector']
coll = db['dishes']

# create a form class
class NewDishForm(FlaskForm):
    dish_name = StringField(' Name of dish you want to add', validators=[DataRequired()])
    dish_type = SelectField('Type of the dish', choices=(coll.find().distinct('dish_type')))
    dish_source = StringField('Where can we find the recepie?')
    submit = SubmitField("Submit")

    def validate_dish_name(form, field):
        dish_exists = coll.find_one({'dish_name': field.data})
        if dish_exists:
            raise ValidationError("dish duplicate")

def change_dish_status(dish_type):
    coll.update_many({'dish_type': dish_type}, {'$set': {'cooked': False}})
    return

@app.route('/', methods=['GET', 'POST'])
def home():
    dishes = coll.find({'cooked': False})
    # reset dishes if all were cooked
    for dish_type in coll.find().distinct('dish_type'):
        if not coll.find_one({'$and':[{'cooked': False}, {'dish_type': dish_type}]}):
            change_dish_status(dish_type)
    if request.method == 'POST':
        dish_type = request.form.get('name')
        return redirect(url_for('pick_meal', dish_type=dish_type))
    return render_template('home.html', dishes=dishes)

@app.route('/pick_meal/<string:dish_type>', methods=['GET', 'POST'])
def pick_meal(dish_type):
    # pick random meal based on category
    dish = list(coll.aggregate([
        {'$match':{
            'cooked': False,
            'dish_type': dish_type}},
        { '$sample':{
            'size': 1 } }]))[0]
    return render_template('pick_meal.html', dish=dish, dish_type=dish_type)

@app.route('/<dish_id>')
def confirm(dish_id):
    coll.update_one({'_id': ObId(dish_id)}, {'$set':{'cooked': True}})
    return redirect(url_for('home'))

@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    form = NewDishForm()
    # validate form
    if form.validate_on_submit():
        if form.errors == {}:
            coll.insert_one({'dish_name': form.dish_name.data, 'dish_type': form.dish_type.data, 'cooked': False, 'dish_source': form.dish_source.data})
            flash('Success, your dish '+form.dish_name.data+' was added!')
        return redirect('/add_dish')
    else:
        # throw error if dish with same name is already in database or other error occured
        for errorMessages in form.errors.values():
            for errorMessage in errorMessages:
                if errorMessage == 'dish duplicate':
                    flash('This dish already exists in database')
                else: flash('Something went wrong')
        return render_template('add_dish.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5000)