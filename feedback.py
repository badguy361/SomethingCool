import sqlite3

connection = sqlite3.connect('feedback.db')


with open('feedback.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO feedback (q1, q2, opinion) VALUES (?,?,?)",
            ('1', '1','1')
            )

cur.execute("INSERT INTO feedback (q1, q2, opinion) VALUES (?,?,?)",
            ('1', '1','1')
            )

connection.commit()
connection.close()
