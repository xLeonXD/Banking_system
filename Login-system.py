import sqlite_data as sql
import time

timing1 = 0.35

def slow_print(text,timing):
    for i in text:
        time.sleep(timing)
        print(i,end="")
    else:
        print("")

def load_accounts():
    items = sql.get_accounts()
    account_dict = {}
    for user_id,username,password in items:
        account_dict[user_id] = Account(user_id,username,password)
    return account_dict

def list_accounts():
    account_dict = load_accounts()
    for i in account_dict:
        print(account_dict[i])

def create_account(usr,pas):
    sql.insert_data_accounts(usr,pas)
    account_dict = load_accounts()

    return account_dict


class Account:
    def __init__(self,user_id,username,password):
        self.user_id  = user_id
        self.username = username
        self.password = password
        self.counter  = 0
        self.login    = False
        self.money    = False

    def login_check(self):
        if self.login:
            return True
        else:
            print("You are not logged in !!")
            return False

    def pay(self,other,pay_amount):
        if not self.login_check():
            return
        sql.pay_transaction(self.user_id,other.user_id,pay_amount,self.username,other.username)

    def update_money_balance(self):
        if not self.login_check():
            return
        pass

    def update_stored_data_money(self):
        money = sql.get_money(self.user_id)
        self.money = money

    def check_money(self):
        if not self.login_check():
            return
        money = sql.get_money(self.user_id)
        print(f"Your balance : {money}")

    def __enter__(self):
        if self.counter > 3:
            print("You have ran out of tries.")
            return self

        print(" Enter username and password.")
        iuser     = input("Username : ")
        ipassword = input("Password : ")
        if iuser == self.username and ipassword == self.password:
            self.login = True
            self.counter = 0
            print("Login Successful")
            return self
        else:
            print("Login Failed.")
            print("Wrong username or password.")
            self.counter += 1
            return self

    def __exit__(self,exc_type, exc_value, traceback):
        self.login = False
        print("Logging out",end="")
        slow_print("...",timing1)
        return self

    def __str__(self):
        return f"{self.user_id} : {self.username}"
account_dict = load_accounts()
list_accounts()

with account_dict[6] as account:
    pass
