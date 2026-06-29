#import sqlite3
import sqlite_data as sql

sql.insert_data_accounts("leon",1234)

def load_accounts():
    """con = sqlite3.connect("accounts.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM accounts")
    """
    #return sql.get_accounts()
    items = sql.get_accounts()
    account_dict = {}
    for user_id,username,password in items:
        account_dict[user_id] = Account(user_id,username,password)
    return account_dict

def list_accounts():
    account_dict = load_accounts()
    for i in account_dict:
        print(account_dict[i])

class Account:
    def __init__(self,user_id,username,password):
        self.user_id  = user_id
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.user_id} : {self.username}"

#print(account_dict)
