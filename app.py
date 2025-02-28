import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)
DATABASE = 'app.db'


def init_db():
    """Создаёт таблицу messages, если она не существует."""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    """Главная страница. 
    - GET: отображает все сообщения и форму для добавления нового.
    - POST: добавляет новое сообщение в базу данных.
    """
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Если метод POST, значит пользователь отправил форму
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            c.execute('INSERT INTO messages (content) VALUES (?)', (content,))
            conn.commit()

    # Получаем все сообщения из базы данных
    c.execute('SELECT * FROM messages')
    messages = c.fetchall()
    conn.close()

    # Формируем простую HTML-страницу с формой и списком сообщений
    html = """
    <html>
      <head>
        <title>Simple Flask App</title>
      </head>
      <body>
        <h1>Messages</h1>
        <form method="POST" action="/">
          <input type="text" name="content" placeholder="Введите сообщение" required />
          <button type="submit">Добавить</button>
        </form>
        <ul>
    """

    for msg in messages:
        html += f"<li>{msg[1]}</li>"

    html += """
        </ul>
      </body>
    </html>
    """
    return html


if __name__ == '__main__':
    init_db()
    # Запускаем приложение на 0.0.0.0, чтобы оно было доступно внутри Docker
    app.run(host='0.0.0.0', port=5000)
