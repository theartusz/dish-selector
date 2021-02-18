import random
import sqlite3
import pandas
from os import system
from os import name

def read_menu(table):
    conn = sqlite3.connect('dishes.db')
    query = 'SELECT * FROM ' + table
    menu = pandas.read_sql(query,conn)
    if len(menu.index) == 0:
        query = 'SELECT * FROM ' + table + '_orig'
        menu = pandas.read_sql(query,conn)
    return menu

def pick_meal(dish_type_df):
    while True:
        menu_len = len(dish_type_df.index)
        meal_choice = random.randint(0, menu_len - 1)
        meal = dish_type_df.iloc[[meal_choice], [1]].to_string(header=False, index=False).strip()
        print('You should make: ' + meal)
        decision = input('[y\\n]: ').lower()
        if decision == 'y':
            popularity = dish_type_df.loc[dish_type_df['dish_name'] == meal, 'popularity'].item()
            if popularity == 1:
                # remove dish from df if popularity is 1
                dish_type_df = dish_type_df[dish_type_df['dish_name'] != meal]
            # decrease popularity
            else: dish_type_df['popularity'][dish_type_df['dish_name'] == meal] = popularity - 1
            return dish_type_df


def add_meal():
    dish_name = input('Dish name: ').lower()
    popularity = int(input('Popularity: '))
    dish_type = input('Disch Type [main\\salat]: ').lower()
    if dish_type == 'main':
        dish_type = 'main_course'

    conn = sqlite3.connect('dishes.db')
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM " + dish_type + "_orig WHERE dish_name = '%s'" % (dish_name))
        if len(c.fetchall()) > 0:
            print('Record already exists in database.\n'
                + 'Do you want to update it?')
            update_record = input('[y/n]: ').lower()
            if update_record == 'y':
                c.execute("UPDATE " + dish_type + "_orig SET popularity = '%s' WHERE dish_name = '%s'" % (popularity, dish_name))
        else: c.execute("INSERT INTO " + dish_type + "_orig (dish_name, popularity) VALUES ('%s', '%s')" % (dish_name, popularity))

# define clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for linux/mac
    else:
        _ = system('clear')

"""
Program start
"""

clear()
main_course_df = read_menu('main_course')
salat_df = read_menu('salat')

print('Hello to the dish selector!')

while True:
    print('\nWhat do you want to do?\n'
        + '[1 - pick a main meal, 4 - options, 5 - add meal, exit]')

    decision = input().lower()

    if decision == '1':
        main_course_df = pick_meal(main_course_df)

    elif decision == '2':
        salat_df = pick_meal(salat_df)

    elif decision == '4':
        print(main_course_df[['dish_name', 'popularity']])
        print(salat_df[['dish_name', 'popularity']])

    elif decision == '5':
        add_meal()

    elif decision == 'exit':
        break