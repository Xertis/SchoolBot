import sqlite3

# Создаем подключение к базе данных (или создаем новую)
conn = sqlite3.connect('database.db')

# Создаем курсор
cursor = conn.cursor()

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()
