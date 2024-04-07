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
from config import DIFFICULTY  # Import the difficulty from config.py

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()
        self.merkle_root = self.compute_merkle_root()
        self.block_header = {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "version_bytes": b'1.0',  # Example version bytes, adjust as needed
            "transactions": [tx.to_obj() for tx in self.transactions]  # List of transaction details
        }

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

    def compute_merkle_root(self):
        if len(self.transactions) == 0:
            return None
        if len(self.transactions) == 1:
            return self.transactions[0].transaction_id

        intermediate_hashes = []

        # Compute the Merkle root from the transaction IDs
        transaction_ids = [transaction.transaction_id for transaction in self.transactions]
        for tx_id in transaction_ids:
            intermediate_hashes.append(hashlib.sha256(tx_id.encode()).hexdigest())

        while len(intermediate_hashes) > 1:
            if len(intermediate_hashes) % 2 != 0:
                intermediate_hashes.append(intermediate_hashes[-1])

            paired_hashes = [intermediate_hashes[i] + intermediate_hashes[i + 1] for i in range(0, len(intermediate_hashes), 2)]
            intermediate_hashes = [hashlib.sha256(pair.encode()).hexdigest() for pair in paired_hashes]

        return intermediate_hashes[0]

    def mine_block(self):
        attempt_count = 0  # Initialize attempt counter
        
        # Special case for the genesis block
        if self.index == 0:
            self.previous_hash = "0"  # Set previous hash to "0"
            while self.hash[:DIFFICULTY] != '0' * DIFFICULTY:
                self.nonce += 1
                self.hash = self.compute_hash()
                attempt_count += 1
                print(f"Attempt {attempt_count}: Hash Result: {self.hash}")

            print("Block mined successfully!")
            return

        # Mine the block with the given difficulty
        while self.hash[:DIFFICULTY] != '0' * DIFFICULTY:
            self.nonce += 1
            self.hash = self.compute_hash()
            attempt_count += 1
            print(f"Attempt {attempt_count}: Hash Result: {self.hash}")

        print("Block mined successfully!")

    def to_obj(self):
        # Serialize the block directly
        return {
            "index": self.index,
            "transactions": [transaction.to_obj() for transaction in self.transactions],
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
            "merkle_root": self.merkle_root
        }

    def serialize(self):
        # Serialize the block using the to_obj method and then use the serialize function
        return serialize(self.to_obj())

    @staticmethod
    def deserialize(serialized_data):
        # Deserialize the serialized data using the deserialize function
        data = deserialize(serialized_data)
        transactions = [Transaction.from_obj(tx) for tx in data['transactions']]
        return Block(data['index'], transactions, data['timestamp'], data['previous_hash'])