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
    for user_id,username,password,temp,temp2,lock_state in items:
        account_dict[user_id] = Account(user_id,username,password,lock_state)
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
    def __init__(self,user_id,username,password,lock_state):
        self.user_id  = user_id
        self.username = username
        self.password = password
        self.counter  = 0
        self.login    = False
        self.locked   = lock_state
        self.money    = False
        #self.pay_amount = False


    def login_check(self):
        if self.locked:
            print("This account is locked.")
            return False
        elif self.login:
            return True
        else:
            print("You are not logged in !!")
            return False

    def check_payment(self,pay_amount):
        if pay_amount <= self.money:
            return True
        else:
            return False

    def pay(self,other,pay_amount):
        if not self.login_check():
            return
        sql.pay_transaction(self.user_id,other.user_id,pay_amount,self.username,other.username)

    def payment_process(self,other,pay_amount):
        self.update_stored_data_money()
        if not self.check_payment(pay_amount):
            print("Not enough money !!")
            return self
        self.pay(other,pay_amount)
        return self

    """def update_money_balance(self):
        if not self.login_check():
            return
        pass"""

    def update_stored_data_money(self):
        money = sql.get_money(self.user_id)
        self.money = money
        return self

    def check_money(self):
        if not self.login_check():
            return
        money = sql.get_money(self.user_id)
        print(f"Your balance : {money}")

    def deposit_withdraw(self):
        self.login_check()
        print("What do you wanna do ? Withdraw / Deposit ")
        choice = input("W/D : ")
        choice = choice.lower()
        if choice == "w" or choice == "withdraw":
            amount_type = -1
            choice = "withdraw"
        elif choice == "d" or choice == "deposit":
            amount_type = 1
            choice = "deposit"
        else:
            print("Invalid choice.")
            return
        print(f"How much money to {choice}? ")
        money_amount = input(" $ : ")
        try:
            money_amount = int(money_amount)
        except Exception as error:
            print(f"Error : {error}")
            print("Money amount was not a number")
            return
        if money_amount <= 0:
            if money_amount == 0:
                print("Money amount is 0$ ")
                return
            elif money_amount < 0:
                print("Money amount can't be negative")
                return
        if choice == "withdraw":
            self.update_stored_data_money()
            if not self.check_payment(money_amount):
                print("Not enough money.")
                return
        money_amount *= amount_type
        sql.change_money(self.user_id,money_amount)
        self.update_stored_data_money()
        return self

    def __enter__(self):
        if self.locked:
            pass
            #return
        if self.counter >= 3:
            self.locked = True
            print("You have ran out of tries.")
            print("Your account is now locked.")
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

#sql.delete_data_accounts(5)
#sql.delete_data_accounts(6)
sql.create_table_accounts()
sql.create_transaction_table()
sql.insert_data_accounts("leon",1234)
account_dict = load_accounts()
list_accounts()
sql.display()


with account_dict[1] as account:
    pass
