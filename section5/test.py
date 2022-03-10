import sqlite3

connection = sqlite3.connect("data.db") # creates a file 
cursor = connection.cursor() # select things and start things.
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, "RC", "1234")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, "alice", "123"),
    (3, "bob", "asdf"),
    (4, "carol", "qwer"),
    (5, "david", "zxcv"),
    (6, "erin", "lalala"),
]
cursor.executemany(insert_query, users)

select_query = "SELECT id, username from users"
for row in cursor.execute(select_query):
    print(row)

connection.commit() # save changes
connection.close()