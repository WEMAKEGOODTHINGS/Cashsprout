import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",   # EMPTY because you don't have a MySQL password
    database="BankDB"
)


cur = con.cursor()

def create_account(acc, name, bal):
    cur.execute("INSERT INTO accounts VALUES(%s,%s,%s)", (acc, name, bal))
    con.commit()

def deposit(acc, amt):
    cur.execute("UPDATE accounts SET balance = balance + %s WHERE account_no=%s", (amt, acc))
    cur.execute("INSERT INTO transactions(account_no,type,amount) VALUES(%s,'deposit',%s)", (acc, amt))
    con.commit()

def withdraw(acc, amt):
    cur.execute("SELECT balance FROM accounts WHERE account_no=%s", (acc,))
    bal = cur.fetchone()[0]
    
    if bal >= amt:
        cur.execute("UPDATE accounts SET balance = balance - %s WHERE account_no=%s", (amt, acc))
        cur.execute("INSERT INTO transactions(account_no,type,amount) VALUES(%s,'withdraw',%s)", (acc, amt))
        con.commit()
        return True
    else:
        return False

def check_balance(acc):
    cur.execute("SELECT balance FROM accounts WHERE account_no=%s", (acc,))
    return cur.fetchone()[0]
