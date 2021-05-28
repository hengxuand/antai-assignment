import sqlite3

conn = sqlite3.connect('antai.db')
cur = conn.cursor()

cur.execute(
    "create table members(id INTEGER PRIMARY KEY, username TEXT, email TEXT)"
)

insert_query = "insert into members (username, email) values (?, ?)"
cur.execute(insert_query, ("hxd", "hengxuad@uci.edu"))
cur.execute(insert_query, ("Nina", "nhatv@uci.edu"))
cur.execute(insert_query, ("Shaun", "shaun@uci.edu"))
cur.execute(insert_query, ("Mike", "mike@uci.edu"))
cur.execute(insert_query, ("Andra", "andra@uci.edu"))
cur.execute(insert_query, ("Matthew", "matthew@uci.edu"))
cur.execute(insert_query, ("Mandy", "mandy@uci.edu"))
cur.execute(insert_query, ("Cindy", "cindy@uci.edu"))
cur.execute(insert_query, ("Rocky", "rocky@uci.edu"))
cur.execute(insert_query, ("Andy", "andy@uci.edu"))
cur.execute(insert_query, ("Brandon", "brandon@uci.edu"))
cur.execute(insert_query, ("Parker", "parker@uci.edu"))
cur.execute(insert_query, ("Joshua", "joshua@uci.edu"))

conn.commit()
cur.close()
