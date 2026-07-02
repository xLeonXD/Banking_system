import sqlite3

def insert_data_accounts(usr,pas):
    #import sqlite3
    #con = sqlite3.connect("accounts.db")
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO accounts (username,password,money) VALUES (?,?,0)",[usr,pas])
            con.commit()
            #con.close()
        except Exception as error:
            print(f"Error : {error}")
            con.rollback()
            print("Something happened, rolling back!!")
            #con.close()

def insert_data_transaction(user_id,username,user_id2,username2,money,money_spent):
    #import sqlite3
    #con = sqlite3.connect("accounts.db")
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?)",[user_id,username,user_id2,username2,money,money_spent])
            con.commit()
            #con.close()
        except Exception as error:
            print(f"Error : {error}")
            con.rollback()
            #con.close()


def delete_data_accounts(user_id):
    #import sqlite3
    #con = sqlite3.connect("accounts.db")
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM accounts WHERE user_id = ?",[user_id])
            con.commit()
            #con.close()
        except Exception as error:
            print(f"Error : {error}")
            con.rollback()
            print("Something happened, rolling back!!")
            #con.close()

def get_money(user_id):
    #import sqlite3
    #con = sqlite3.connect("accounts.db")
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT money FROM accounts WHERE user_id = ? ",[user_id])
        money_tuple = cursor.fetchone()
        money = money_tuple[0]
        #con.close()
        return money

def change_money(user_id,money):
    #import sqlite3
    #con = sqlite3.connect("accounts.db")
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE accounts SET money = ? WHERE user_id = ?",[money,user_id])
            con.commit()
            #con.close()
        except Exception as error:
            print(f"Error : {error}")
            print("Transaction failed !!")
            con.rollback()
            #con.close()

def change_lock_state(user_id,state):
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE accounts SET lock_state = ? WHERE user_id = ?",[state,user_id])
            con.commit()
        except Exception as error:
            print(f"Error : {error}")
            print("Acount lock state management failure")
            con.rollback()

def pay_transaction(user_id1,user_id2,pay_amount,username1,username2):
    #import sqlite3
    #con = sqlite3.connect("accounts.db")
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()

        """money_1 = get_money(user_id1)
        money_1 = money_1 - pay_amount
        money_2 = get_money(user_id2)
        money_2 = money_2 + pay_amount"""

        cursor.execute("SELECT money FROM accounts WHERE user_id = ?", [user_id1])
        money_1 = cursor.fetchone()[0]
        cursor.execute("SELECT money FROM accounts WHERE user_id = ?", [user_id2])
        money_2 = cursor.fetchone()[0]

        new_money_1 = money_1 - pay_amount
        new_money_2 = money_2 + pay_amount

        """try:
            change_money(user_id1,money_1)
            change_money(user_id2,money_2)
            con.commit()
            con.close()
        except:
            con.rollback()
            con.close()"""

        try:
            cursor.execute("UPDATE accounts SET money = ? WHERE user_id = ?", [new_money_1, user_id1])
            cursor.execute("UPDATE accounts SET money = ? WHERE user_id = ?", [new_money_2, user_id2])
            cursor.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?)",[user_id1, username1, user_id2, username2, new_money_1, -pay_amount])
            cursor.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?)",[user_id2, username2, user_id1, username1, new_money_2, +pay_amount])
            con.commit()
            #con.close()

        except Exception as error:
            print(f"Error : {error}")
            print("Transaction failed !!")
            con.rollback()
            #con.close()

def create_transaction_table():
    #import sqlite3
    #con = sqlite3.connect("accounts.db")
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS transactions( 
                        user_id     INT NOT NULL,
                        username    TEXT NOT NULL,           
                        user_id2    INT NOT NULL,
                        username2   TEXT NOT NULL,
                        money       INT NOT NULL,
                        money_spent INT NOT NULL,
                        transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
                        )""")
        con.commit()
        #con.close()

def create_table_accounts():
    #import sqlite3
    #con = sqlite3.connect("accounts.db")
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS accounts(
                       user_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL UNIQUE,
                       password TEXT NOT NULL,
                       money    INT NOT NULL,
                       account_created_time TEXT DEFAULT CURRENT_TIMESTAMP,
                       lock_state BOOL DEFAULT FALSE
                       )""")
        con.commit()
        #con.close()

#import_data_accounts("leoner11",1234)
#delete_data_accounts(1)
def display():
    #import sqlite3
    #con = sqlite3.connect("accounts.db")
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM accounts")
        items = cursor.fetchall()
        for i in items:
            print(i)
            #print("a")
        #con.close()

def get_accounts():
    #import sqlite3
    #con = sqlite3.connect("accounts.db")
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM accounts")
        items = cursor.fetchall()
        #con.close()
        return items

def get_transactions(user_id,amount=10):
    with sqlite3.connect("accounts.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY transaction_date DESC",[user_id])
        transaction_tuple = cursor.fetchmany(amount)
        return transaction_tuple

#insert_data_accounts("leon2","1234")
#display()

