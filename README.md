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
set -x FLASK_APP app
set -x FLASK_DEBUG True
```
- run Flask by executing:
```
flask run
```