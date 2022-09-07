import sqlite3

connection = sqlite3.connect('base.db')


with open('base.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO base (deep_sleep, light_sleep, sleep_time, sleep_status) VALUES (?,?,?,?)",
            ('1', '1','new','new')
            )

cur.execute("INSERT INTO base (deep_sleep, light_sleep, sleep_time, sleep_status) VALUES (?,?,?,?)",
            ('1', '1','new','new')
            )

connection.commit()
connection.close()

#執行這個會啟動.sql讓前面post的資料不見