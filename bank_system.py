import mysql.connector

class BankSystem:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kanikakanika22@",  # replace with your MySQL password
            database="bankdb"
        )
        self.cursor = self.db.cursor()

    # Create account
    def create_account(self, acc_id, name, username, pin, balance):
        try:
            sql = "INSERT INTO accounts (id, name, username, pin, balance) VALUES (%s,%s,%s,%s,%s)"
            val = (acc_id, name, username, pin, balance)
            self.cursor.execute(sql, val)
            self.db.commit()
            return True, "Account created successfully!"
        except mysql.connector.IntegrityError:
            return False, "Account ID or Username already exists!"
        except Exception as e:
            return False, str(e)

    # Authenticate login
    def authenticate(self, username, pin):
        sql = "SELECT id FROM accounts WHERE username=%s AND pin=%s"
        self.cursor.execute(sql, (username, pin))
        res = self.cursor.fetchone()
        if res:
            return res[0]  # account ID
        return None

    # Get balance
    def get_balance(self, acc_id):
        sql = "SELECT balance FROM accounts WHERE id=%s"
        self.cursor.execute(sql, (acc_id,))
        res = self.cursor.fetchone()
        if res:
            return True, res[0]
        return False, 0

    # Deposit money
    def deposit(self, acc_id, amount):
        if amount <= 0:
            return False, "Deposit amount must be >0"
        sql = "UPDATE accounts SET balance = balance + %s WHERE id=%s"
        self.cursor.execute(sql, (amount, acc_id))
        self.db.commit()
        return True, f"₹ {amount} deposited successfully"

    # Withdraw money
    def withdraw(self, acc_id, amount):
        sql = "SELECT balance FROM accounts WHERE id=%s"
        self.cursor.execute(sql, (acc_id,))
        res = self.cursor.fetchone()
        if not res:
            return False, "Account not found"
        if amount > res[0]:
            return False, "Insufficient balance"
        sql = "UPDATE accounts SET balance = balance - %s WHERE id=%s"
        self.cursor.execute(sql, (amount, acc_id))
        self.db.commit()
        return True, f"₹ {amount} withdrawn successfully"

    # Get transactions (dummy example, extend as needed)
    def get_transactions(self, acc_id):
        sql = "SELECT id, 'Deposit', balance, NOW() FROM accounts WHERE id=%s"
        self.cursor.execute(sql, (acc_id,))
        return self.cursor.fetchall()
