# Dish Selector

## Development
- create virtual environment
- activate the virtual environment
```
. flask-app/bin/activate.fish
```
- install dependencies from `pip_freeze` file
- create env variables for Flask (for fish):
```
set -x FLASK_APP app/app
set -x FLASK_DEBUG True
```
- create .env file in `app` folder and define app secrets like `MONGODB_USER`, `MONGODB_PASSWORD` and `SECRET_KEY`
- run Flask by executing:
```
flask run
```