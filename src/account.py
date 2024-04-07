# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

from transaction import Transaction, CoinbaseTransaction
import mempool
from amount import Amount  # Import the Amount class
from db import Database

import sqlite3

# Connect to the database
connection = sqlite3.connect('wallets.db')
cursor = connection.cursor()

# Check if the 'accounts' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")
table_exists = cursor.fetchone()

if not table_exists:
    # Create the 'accounts' table if it doesn't exist
    cursor.execute('''CREATE TABLE accounts
                      (passphrase TEXT, public_key_hash TEXT, wallet_address TEXT, amount REAL, account_type TEXT)''')
    connection.commit()
    print("Table 'accounts' created.")

    # Add the 'amount_currency' column
    cursor.execute("ALTER TABLE accounts ADD COLUMN amount_currency TEXT")
    connection.commit()
    print("Column 'amount_currency' added to the accounts table.")
else:
    print("Table 'accounts' already exists.")

# Close the connection
connection.close()

class Account:
    def __init__(self, passphrase, public_key_hash, wallet_address, amount, account_type):
        self.passphrase = passphrase
        self.public_key_hash = public_key_hash
        self.wallet_address = wallet_address
        self.amount = amount  # Assuming 'amount' is an instance of the 'Amount' class
        self.account_type = account_type
        
    def to_obj(self):
        amount_obj = self.amount.to_obj()
        return {
            "passphrase": self.passphrase,
            "public_key_hash": self.public_key_hash,
            "wallet_address": self.wallet_address,
            "amount_value": self.amount.value,  # Use 'value' attribute
            "amount_currency": self.amount.currency,  # Use 'currency' attribute
            "account_type": self.account_type
        }

    def deposit(self, amount):
        # Add the deposited amount to the account balance
        self.amount += amount

    def withdraw(self, amount):
        # Check if there are sufficient funds before withdrawal
        if self.amount >= amount:
            self.amount -= amount
            return True
        else:
            print("Insufficient funds.")
            return False

    def get_balance(self):
        return self.amount
    
    def save_to_database(self, db):
        db.insert_account(self)
        return self  # Return self instead of a dictionary

    @staticmethod
    def from_obj(data):
        amount = Amount.from_obj(data["amount"])
        return Account(data["passphrase"], data["public_key_hash"], data["wallet_address"], amount, data["account_type"])

    def create_transaction(self, recipient, amount):
        # Create a new transaction object
        transaction = Transaction(self.wallet_address, recipient, amount)
        return transaction

    def broadcast_transaction(self, transaction):
        # Broadcast the transaction to the mempool
        transaction.broadcast_to_mempool()