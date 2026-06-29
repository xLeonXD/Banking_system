import sqlite3

con = sqlite3.connect("accounts.db")
cursor = con.cursor()

def insert_data_accounts(usr,pas):
    try:
        cursor.execute("INSERT INTO accounts (username,password) VALUES (?,?)",[usr,pas])
        con.commit()
    except:
        con.rollback()
        print("Something happened, rolling back!!")

def delete_data_accounts(id):
    try:
        cursor.execute("DELETE FROM accounts WHERE user_id = (?)",[id])
        con.commit()
    except:
        con.rollback()
        print("Something happened, rolling back!!")
def create_table():
    cursor.execute("""CREATE TABLE accounts(
                   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL
                   )""")

#import_data_accounts("leoner11",1234)
#delete_data_accounts(1)

cursor.execute("SELECT * FROM ACCOUNTS")

items = cursor.fetchall()
for i in items:
    print(i)
    print("a")


