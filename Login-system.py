import sqlite_data as sql
import time
import bcrypt

"""
To do list:
account creation: - DONE -
    add a func to add accounts.

faster account loading: - DONE -
    instead of loading all of the accounts, load a specific one 
    using the id and check the db and then load it into here.

get transactions for the user: - DONE -
    the function exist just add it in login system.
    
deleting accounts: - DONE -
    add a way for users to deleting accounts.

a way for the user to unlock accounts: - DONE -
    self explanatory. 

password hashing:
    maybe not rn but would be nice. 
"""

timing1 = 0.35
account_dict = {}

def slow_print(text,timing):
    for i in text:
        time.sleep(timing)
        print(i,end="")
    else:
        print("")

def load_accounts(account_dict=None):
    if account_dict is None:
        account_dict = {}
    items = sql.get_accounts()
    #account_dict = {}
    for user_id,username,password,temp,temp2,lock_state in items:
        account_dict[user_id] = Account(user_id,username,password,lock_state)
    return account_dict

def list_all_accounts():
    account_dict = load_accounts()
    for i in account_dict:
        print(account_dict[i])

def list_accounts_cached(account_dict):
    #account_dict = load_accounts(account_dict)
    for i in account_dict:
        print(account_dict[i])

def hashing(pas):
    byte = pas.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = (byte,salt)
    return hash

def create_byte(pas):
    byte = pas.encode("utf-8")
    return byte

def create_account(usr,pas,account_dict=None):
    hash_pas = hashing(pas)
    sql.insert_data_accounts(usr,hash_pas)
    user_id = sql.get_id(usr)
    if account_dict is None:
        account_dict = {}
    account_dict,_ = load_specific_account(account_dict,user_id)
    return account_dict,user_id

def load_specific_account(account_dict,user_id):
    if user_id in account_dict:
        print("Found")
        return account_dict,True
    item = sql.get_one_account(user_id)
    if item is None:
        print("Account not found.")
        return account_dict,False
    print(f"item : {item}")
    _,username,password,temp,temp2,lock_state = item
    print(f"_ : {_}")
    account_dict[_] = Account(user_id,username,password,lock_state)
    return account_dict,True

def unlock(account_dict):
    print("insert ID")
    user_id = input("ID : ")
    try:
        user_id = int(user_id)
    except ValueError:
        print("ID must be a number")
        time.sleep(0.35)
        return
    account_dict,proceed = load_specific_account(account_dict,user_id)
    if not proceed:
        print("ID not found")
        return account_dict
    account_dict[user_id].locked = False
    sql.change_lock_state(user_id,False)
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
        if not self.login_check():
            return
        if self.user_id == other.user_id:
            print("You cannot pay yourself.")
            return self
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
        if not self.login_check():
            return
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
        sql.change_money(self.user_id,money_amount,self.username)
        self.update_stored_data_money()
        return self

    def transaction_list(self):
        if not self.login_check():
            return
        transaction_tuple = sql.get_transactions(self.user_id,100)
        for i in transaction_tuple:
            user_id,name,user_id2,name2,money,money_difference,date,transaction_type,index = i
            #print(i)
            print(f"""
                    ID : {user_id} - Name : {name} | {transaction_type} ID : {user_id2} - Name : {name2}
                    Balance : {money} - Money exchanged amount : {money_difference} 
                    Date : {date}   - Index : {index}
            """)

    def delete_account(self):
        if not self.login_check():
            return
        print("Are you sure you want to close your account ?")
        ans = input("Y/n : ")
        if ans == "y" or ans == "yes":
            sql.delete_data_accounts(self.user_id)
            self.login = False
            print("Account closed.")
            #self.__exit__(None, None, None)
            return True
        else:
            print("Account deletion canceled.")
            return False

    def check_person(self):
        if not self.login_check():
            return
        self.update_stored_data_money()
        date = sql.get_date(self.user_id)
        print(f"""
            ID : {self.user_id}  ---  Name : {self.username} --- Balance : {self.money}                                                                                 
            Account creation date : {date}                                                                                                                                                                  
        """)

    def __enter__(self):
        while True:
            if self.locked:
                print("Account is locked.")
                return
            if self.counter >= 3:
                self.locked = True
                sql.change_lock_state(self.user_id,self.locked)
                print("You have ran out of tries.")
                print("Your account is now locked.")
                return self
            print(" Enter username and password.")
            iuser     = input("Username : ")
            ipassword = input("Password : ")
            new_pas = create_byte(ipassword)
            result = bcrypt.checkpw(new_pas,self.password)
            if iuser == self.username and ipassword == self.password:
                self.login = True
                self.counter = 0
                print("Login Successful")
                return self
            else:
                print("Login Failed.")
                print("Wrong username or password.")
                self.counter += 1
                #return self

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
"""create_account("bomb","lego")
account_dict = load_specific_account(account_dict,3)
print(account_dict)
#account_dict = load_accounts()
#list_all_accounts()"""
sql.display()


"""with account_dict[2] as account:
    #account.deposit_withdraw()

    account.payment_process(account_dict[2],200)
    account.transaction_list()
    account.payment_process(account_dict[1],1)
    account.payment_process(account_dict[1], 20)
    account.payment_process(account_dict[1], 100)
    account.payment_process(account_dict[1], 0)
    account.payment_process(account_dict[1], 1)
    account.payment_process(account_dict[1], 2)
    account.payment_process(account_dict[1], 3)
    account.payment_process(account_dict[1], 4)
    account.payment_process(account_dict[1], 5)
    account.payment_process(account_dict[1], 6)
    account.payment_process(account_dict[1], 7)
    account.payment_process(account_dict[1], 8)
    account.payment_process(account_dict[1], 9)
    account.payment_process(account_dict[1], 10)

    pass"""

choice = ["1","2","3","4","5","login","log into bank account","create account","get id","exit"]
choice2 = ["1","2","3","4","5","6","7"]
while True:
    print("What do you wanna do ? ")
    print("""    1 ) Log into bank account
    2 ) Create Account
    3 ) Get ID
    4 ) Unlock Account
    5 ) Exit
    """)
    ichoice = input(" ? : ")
    if not ichoice in choice:
        print("Wrong choice.")
        time.sleep(0.35)
        continue

    if ichoice == "1" or ichoice == "login" or ichoice == "log into bank account":
        ichocie = "login"

    elif ichoice == "2" or ichoice == "create account":
        ichocie = "create"
        print("Please type in an username.")
        username = input("username : ")
        print("Please type in a password.")
        password = input("password : ")
        account_dict,user_id = create_account(username,password)
        print(f"your ID is : {user_id}")
        time.sleep(1)
        continue

    elif ichoice == "3" or ichoice == "get id":
        ichoice = "ID"
        print("Please type in the username")
        username = input(f"username : ")
        user_id = sql.get_id(username)
        if user_id is None:
            print("ID not found")
            continue
        print(f"{username}'s ID is {user_id}")
        time.sleep(1)
        continue

    elif ichoice == "4":
        account_dict = unlock(account_dict)
        time.sleep(1)
        continue

    elif ichoice == "5" or ichoice == "exit":
        print("Exiting",end="")
        slow_print("...",timing1)
        exit()

    print("Please enter your ID")
    user_id = input("ID : ")
    try:
        user_id = int(user_id)
    except ValueError:
        print("ID must be a number")
        time.sleep(0.35)
        continue
    account_dict,proceed = load_specific_account(account_dict,user_id)
    if not proceed:
        time.sleep(0.35)
        continue
    with account_dict[user_id] as account:
        if not account.login_check():
            continue
        action = True
        while action:
            print("What do you wanna do ?")
            print("""    1) Withdraw / Deposit
    2) Pay 
    3) Check balance
    4) Check profile
    5) Get transaction list
    6) Delete account
    7) Log out
             """)
            ichoice2 = input("? : ")
            if not ichoice2 in choice2:
                print("Wrong choice.")
                time.sleep(0.35)
                continue
            if ichoice2 == "1":
                ichoice2 = "Withdraw_Deposit"
                account.deposit_withdraw()

            elif ichoice2 == "2":
                ichoice2 = "Pay"
                print("Please type in the ID of the person you want to pay.")
                id2 = input("ID : ")
                try:
                    id2 = int(id2)
                except ValueError:
                    print("ID must be a number")
                    time.sleep(0.35)
                    continue
                account_dict, proceed = load_specific_account(account_dict, id2)
                if not proceed:
                    time.sleep(0.35)
                    continue
                print("How much ?")
                amount = input(" $ : ")
                try:
                    amount = int(amount)
                except ValueError:
                    print("Pay amount must be a number")
                    time.sleep(0.35)
                    continue
                account.payment_process(account_dict[id2],amount)
                time.sleep(1)
                continue

            elif ichoice2 == "3":
                account.check_money()
                time.sleep(1)
                continue

            elif ichoice2 == "4":
                account.check_person()
                time.sleep(1)
                continue

            elif ichoice2 == "5":
                account.transaction_list()
                time.sleep(1)
                continue

            elif ichoice2 == "6":
                ichoice = "delete"
                if account.delete_account():
                    action = False
                    break

            elif ichoice2 == "7":
                action = False
                break
