import sqlite3
import os
import pandas as pd

def menu_prompt(menu_choice,start):
    ##os.system('cls')
    if start == 0:
        print('\nWelcome to Key Value in memory!\n\n')
        print('1. Enter a new Key Pair value')
        print('2. Read an existing Key Pair value')
        print('3. Show all Key Values in file')
        print('4. Exit')

        start = 1
    else:
        print('1. Enter a new Key Pair value')
        print('2. Read an existing Key Pair value')
        print('3. Show all Key Values in file')
        print('4. Exit')
    try:
        menu_choice = int(input('\nEnter a Menu Option: ').strip())
        if (menu_choice) < 0 or menu_choice > 4:
            print('invalid option, try again')
            menu_choice,start = menu_prompt(menu_choice, start)
    except ValueError:
        print('Invalid input, Use only Numbers')
        menu_choice,start = menu_prompt(menu_choice,start)


    #os.system('cls')
    return menu_choice,start


def insert_data(curr):
    # Get Key & Pair Value from User
    Key = input('Enter Key: ').strip()
    Value = input('Enter Value: ').strip()

    # check if value previously exist in database
    SQL = f'Select * from Key_Value where Key = "{Key}"'
    curr.execute(SQL)
    data = curr.fetchone()
    if data is None:
        # insert new value
        print('Inserting New Key..\n\n')
        SQL = f'Insert into Key_Value values("{Key}","{Value}")'
        curr.execute(SQL)
    else:
        # Replacing old Key Value Pair with new
        print('Previous Key Value Found, Replacing with new input\n\n')
        SQL = f'Update Key_Value set Value = "{Value}" where Key = "{Key}"'
        curr.execute(SQL)


def read_data(read_value, curr):
    # finding value from key
    SQL = f'Select * from Key_Value where Key = "{read_value}"'
    curr.execute(SQL)
    data = curr.fetchone()

    if data is None:
        # No key found
        print('Key not found\n\n')
    else:
        # Key is found, print to screen
        print(f'Key was found!')
        print(f'Key: {data[0]}\nValue: {data[1]}\n\n')


if __name__ == '__main__':
    # database connection
    conn = sqlite3.connect('Data.db')
    cur = conn.cursor()

    # menu Prompt
    menu_choice = 0
    start = 0
    while menu_choice != 4:
        menu_choice,start = menu_prompt(menu_choice,start)
        if menu_choice == 1:
            insert_data(cur)
        elif menu_choice == 2:
            read_value = input('\nEnter Key: ').strip()
            read_data(read_value,cur)
        elif menu_choice == 3:
            SQL = 'Select * from Key_Value'
            cur.execute(SQL)
            data = cur.fetchall()
            data = pd.DataFrame(data, columns=['Key', 'Value'])
            print(data)
    print('\n\nExiting Program... Memory is persistent in database')
    conn.commit()
    cur.close()
