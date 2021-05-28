import sqlite3

conn = sqlite3.connect('antai.db')
cur = conn.cursor()

cur.execute(
    "create table members(id INTEGER PRIMARY KEY, username TEXT, email TEXT)"
)

insert_query = "insert into members (username, email) values (?, ?)"
cur.execute(insert_query, ("hxd", "hengxuad@uci.edu"))

conn.commit()
cur.close()
