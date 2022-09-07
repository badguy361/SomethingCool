import sqlite3

connection = sqlite3.connect('signin1.db')


with open('signin.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO signin (username, email) VALUES (?, ?)",
            ('First signin', 'Content for the first signin')
            )

cur.execute("INSERT INTO signin (username, email) VALUES (?, ?)",
            ('Second signin', 'Content for the second signin')
            )

connection.commit()
connection.close()

#執行這個會啟動signin.sql讓前面post的資料不見