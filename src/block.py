# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

import hashlib
from serialized import serialize, deserialize
from time import time
from transaction import Transaction, CoinbaseTransaction
from config import blockchain_config
from datetime import datetime

class Block:
    def __init__(self, index, transactions, previous_hash=None):
        self.index = index
        self.transactions = transactions
        self.timestamp = time()  # Set timestamp to current time
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()
        self.max_block_size = blockchain_config.max_block_size
        self.block_interval = blockchain_config.block_interval
        self.block_header = {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "version_bytes": b'1.0',  # Example version bytes, adjust as needed
            "transactions": [tx.to_obj() for tx in self.transactions]  # List of transaction details
        }

    def validate_block_size(self):
        # Check if the size of the block exceeds the maximum block size
        block_size = len(self.serialize())
        return block_size <= self.max_block_size

    def validate_block_interval(self, previous_block_timestamp):
        # Check if the time between this block and the previous block exceeds the block interval
        time_diff = self.timestamp - previous_block_timestamp
        return time_diff >= self.block_interval

    def compute_hash(self):
        # Serialize the block header directly
        block_header = {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "version_bytes": b'1.0',  # Example version bytes, adjust as needed
            "transactions": [tx.to_obj() for tx in self.transactions]  # List of transaction details
        }
        return hashlib.sha256(serialize(block_header)).hexdigest()
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def mine_block(self):
        attempt_count = 0  # Initialize attempt counter
            
        # Mine the block with the given difficulty
        while self.hash[:blockchain_config.difficulty] != '0' * blockchain_config.difficulty:
            self.nonce += 1
            self.hash = self.compute_hash()
            attempt_count += 1
            print(f"Attempt {attempt_count}: Hash Result: {self.hash}")

        print("Block mined successfully!")  # Print the success message after mining

        # Format the timestamp after mining
        self.timestamp_str = datetime.utcfromtimestamp(self.timestamp).strftime('%d %b %y %H:%M:%S')

    def to_obj(self):
        # Serialize the block directly
        return {
            "index": self.index,
            "transactions": [transaction.to_obj() for transaction in self.transactions],
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
            "merkle_root": self.merkle_root  # You can remove this line
        }

    def serialize(self):
        # Serialize the block using the to_obj method and then use the serialize function
        return serialize(self.to_obj())

    @staticmethod
    def deserialize(serialized_data):
        # Deserialize the serialized data using the deserialize function
        data = deserialize(serialized_data)
        transactions = [Transaction.from_obj(tx) for tx in data['transactions']]
        return Block(data['index'], transactions, data['previous_hash'])