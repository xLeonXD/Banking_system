def insert_data_accounts(usr,pas):
    import sqlite3
    con = sqlite3.connect("accounts.db")
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO accounts (username,password,money) VALUES (?,?,0)",[usr,pas])
        con.commit()
        con.close()
    except:
        con.rollback()
        print("Something happened, rolling back!!")
        con.close()

def delete_data_accounts(user_id):
    import sqlite3
    con = sqlite3.connect("accounts.db")
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM accounts WHERE user_id = ?",[user_id])
        con.commit()
        con.close()
    except:
        con.rollback()
        print("Something happened, rolling back!!")
        con.close()

def get_money(user_id):
    import sqlite3
    con = sqlite3.connect("accounts.db")
    cursor = con.cursor()
    cursor.execute("SELECT money FROM accounts WHERE user_id = ? ",[user_id])
    money = cursor.fetchone()
    return money

def create_table_accounts():
    import sqlite3
    con = sqlite3.connect("accounts.db")
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE accounts(
                   user_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL,
                   money    INT NOT NULL
                   )""")
    con.commit()
    con.close()

#import_data_accounts("leoner11",1234)
#delete_data_accounts(1)
def display():
    import sqlite3
    con = sqlite3.connect("accounts.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM accounts")
    items = cursor.fetchall()
    for i in items:
        print(i)
        #print("a")
    con.close()

def get_accounts():
    import sqlite3
    con = sqlite3.connect("accounts.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM accounts")
    items = cursor.fetchall()
    con.close()
    return items


#insert_data_accounts("leon2","1234")
#display()
