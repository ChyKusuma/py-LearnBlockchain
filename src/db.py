# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()  # Call create_table() method here

    def create_table(self):
        self.cursor.execute('''DROP TABLE IF EXISTS accounts''')  # Drop the existing table if it exists
        self.cursor.execute('''CREATE TABLE accounts (
                                passphrase TEXT,
                                public_key_hash TEXT,
                                wallet_address TEXT PRIMARY KEY,
                                amount_value REAL,  -- Add this line to create the amount_value column
                                amount_currency TEXT,
                                account_type TEXT
                                )''')
        self.connection.commit()

    def insert_account(self, account):
        amount_obj = account.amount.to_obj()  # Extract amount object
        amount_value = amount_obj['value']    # Extract amount value
        amount_currency = amount_obj['currency']  # Extract amount currency

        self.cursor.execute('''INSERT OR IGNORE INTO accounts (passphrase, public_key_hash, wallet_address, amount_value, amount_currency, account_type)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                            (account.passphrase, account.public_key_hash,
                            account.wallet_address, amount_value, amount_currency, account.account_type))
        self.connection.commit()

    def insert_block(self, block):
        self.cursor.execute('''INSERT INTO blocks (index, timestamp, previous_hash, nonce, hash, merkle_root)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                            (block.index, block.timestamp, block.previous_hash, block.nonce, block.hash, block.merkle_root))
        self.connection.commit()

    def check_account_exists(self, wallet_address):
        self.cursor.execute("SELECT * FROM accounts WHERE wallet_address=?", (wallet_address,))
        return self.cursor.fetchone() is not None

    def close(self):
        self.connection.close()