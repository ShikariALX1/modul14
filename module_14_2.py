import sqlite3

conn = sqlite3.connect('not_telegram.db')
cursor = conn.cursor()

# удалите из базы данных запись с id = 6
cursor.execute('DELETE FROM Users WHERE id = 6')

# подсчет общего количества записей
cursor.execute('SELECT count(*) FROM Users')

# подсчет сумм всех балансов
cursor.execute('SELECT SUM(balance) FROM Users')

# вывод в консоль среднего баланса всех пользователей
cursor.execute('SELECT AVG(balance) FROM Users')
print(cursor.fetchall())
conn.commit()
conn.close()
