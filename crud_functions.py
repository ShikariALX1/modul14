import sqlite3


def initiate_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Products
                 (id INTEGER PRIMARY KEY,
                 title TEXT NOT NULL,
                 description TEXT,
                 price INTEGER NOT NULL
                 )''')
    #    c.execute('INSERT INTO Products (title, description, price) VALUES (?,?,?)',
    #              ('Продукт1', 'товар с запахом уносящим в детство' , 100))
    #    c.execute('INSERT INTO Products (title, description, price) VALUES (?,?,?)',
    #              ('Продукт2', 'товар с запахом уносящим в детство' , 200))
    #    c.execute('INSERT INTO Products (title, description, price) VALUES (?,?,?)',
    #              ('Продукт3', 'товар с запахом уносящим в детство', 300))
    #    c.execute('INSERT INTO Products (title, description, price) VALUES (?,?,?)',
    #              ('Продукт4', 'товар с запахом уносящим в детство', 400))
    c.execute('CREATE TABLE IF NOT EXISTS Users ('
              'id INTEGER PRIMARY KEY,'
              'username  TEXT NOT NULL,'
              'email  TEXT NOT NULL,'
              'age INTEGER NOT NULL,'
              'balance INTEGER NOT NULL)')
    conn.commit()
    conn.close()


def get_all_products():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Products")
    products = c.fetchall()
    conn.close()
    return products


def add_user(username, email, age):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)",
              (username, email, age, 1000))
    conn.commit()
    conn.close()


def is_included(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Users WHERE username = ?",
              (username,))
    user = c.fetchone()
    if user is None:
        conn.close()
        return False
    else:
        conn.commit()
        conn.close()
        return True
