import sqlite3

# создает базу данных (отработает 1 раз)
connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Users ('
               'id INTEGER PRIMARY KEY,'
               'username  TEXT NOT NULL,'
               'email  TEXT NOT NULL,'
               'age INTEGER,'
               'balance TEXT NOT NULL)')

# заполнит 10 записями (нужно коммитить, отработает каждый запуск)
for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'User{i}', f'example{i}@gmail.com', f'{i}0', 1000))

# обновит balance у каждой 2ой записи начиная с 1ой на 500 (нужно коммитить, отработает каждый запуск)
connection.execute('UPDATE Users SET balance = 500 WHERE id % 2')

# удалит каждую 3ую запись в таблице начиная с 1ой (нужно коммитить, отработает каждый запуск)
cursor.execute('DELETE FROM Users WHERE id % 3 = 1')

# выборка всех записей, где возраст не равен 60, вывод в консоль
cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
users = cursor.fetchall()
for user in users:
    print(user)
connection.commit()
connection.close()
