import sqlite3

connection = sqlite3.connect('users.db')
cursor = connection.cursor()


def initiate_db():
    #cursor.execute(''
                  # 'CREATE TABLE IF NOT EXISTS Products('
                   #'id INTEGER PRIMARY KEY,'
                  # 'title TEXT NOT NULL,'
                  # 'description TEXT,'
                  # 'price INTEGER NOT NULL)''')

    #for i in range(1, 5):
        #cursor.execute(
           # 'INSERT INTO Products(title, description, price) VALUES(?, ?, ?)',
           # (f'Продукт {i}', f'Описание {i}', f'{i * 100}'))

    cursor.execute(''
                   'CREATE TABLE IF NOT EXISTS Users('
                   'id INTEGER PRIMARY KEY,'
                   'username TEXT NOT NULL,'
                   'email TEXT NOT NULL,'
                   'age INTEGER NOT NULL,'
                   'balance INTEGER NOT NULL)''')

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users(email)")


initiate_db()


def add_user(username, email, age):
    cursor.execute(
        'INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
        (f'{username}', f'{email}', age, 1000))


def is_included(username):
    check_users = cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    if check_users.fetchone():
        return True
    else:
        return False


#def get_all_products():
   # cursor.execute('SELECT * FROM Products')
    #products = cursor.fetchall()
   # return products


connection.commit()
