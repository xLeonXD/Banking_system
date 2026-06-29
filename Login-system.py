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
        self.counter  = 0
        self.login    = False

    def __str__(self):
        return f"{self.user_id} : {self.username}"

    def __enter__(self):
        if self.counter > 3:
            print("You have ran out of tries.")
            return

        print(" Enter username and password.")
        iuser     = input("Username : ")
        ipassword = input("Password : ")
        if iuser == self.username and ipassword == self.password:
            self.login = True
            self.counter = 0
            print("Login Successful")
        else:
            print("Login Failed.")
            print("Wrong username or password.")
            self.counter += 1
            return
        
#print(account_dict)
