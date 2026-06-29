import sqlite3

class Account:
    def __init__(self,user_id,username,password):
        self.user_id  = user_id
        self.username = username
        self.password = password

    def load_accounts(self):
        con = sqlite3.connect("accounts.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM accounts")

