# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

import time
from datetime import datetime
from db import Database
from block import Block
from serialized import serialize, deserialize
from trees import MerkleTree
from config import blockchain_config
from uint256 import uint256
from transaction import CoinbaseTransaction

# Define the Blockchain class
class Blockchain:
    def __init__(self, db):
        # Initialize the blockchain with an empty chain and list of pending transactions
        self.chain = []
        self.pending_transactions = []
        self.db = db  # Database instance
        
        # Create and mine the genesis block if the chain is empty
        if not self.chain:
            self.create_genesis_block()

    def create_genesis_block(self):
        # Manually create the genesis block with index 0 and an empty list of transactions
        genesis_block = Block(0, [])  # No previous hash for the genesis block
        genesis_block.mine_block()  # Mine the genesis block
        self.chain.append(genesis_block)
        print("Genesis block mined successfully and added to the chain.")

    def create_new_block(self):
        # Create a new block with the current chain length as the index
        # and the list of pending transactions as its transactions
        new_block = Block(len(self.chain), self.pending_transactions, self.chain[-1].hash)
        return new_block

    def mine_pending_transactions(self):
        # Create a new block using the pending transactions
        new_block = self.create_new_block()

        # Mine the new block
        self.mine_block(new_block)

        # Clear the list of pending transactions
        self.pending_transactions = []

    def mine_block(self, new_block):
        # Mine the block
        hash_attempts = []  # List to store hash attempts
        attempt_count = 1  # Counter for attempts
        while True:
            new_block.hash = new_block.compute_hash()  # Compute the hash
            hash_attempts.append(new_block.hash)  # Append the hash to the list of attempts

            print(f"Attempt {attempt_count}: Hash Result: {new_block.hash}", flush=True)

            # Check if the hash meets the proof of work criteria
            if new_block.hash.startswith('0' * blockchain_config.difficulty):
                print("Block mined successfully!", flush=True)
                break
            else:
                new_block.nonce += 1  # Increment the nonce
                attempt_count += 1

        self.chain.append(new_block)  # Add the mined block to the chain

    def display_chain(self):
        # Display the entire blockchain
        for block in reversed(self.chain):
            self.display_block(block)

    def display_block(self, block):
        # Display information about a specific block
        if block.index == 0:
            block_type = "Genesis Block"
        else:
            block_type = "Block"
            
        print(f"{'-' * 10} {block_type} {block.index} {'-' * 10}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("Transactions:")
        for transaction in block.transactions:
            self.display_transaction(transaction)
        print(f"Timestamp: {datetime.utcfromtimestamp(block.timestamp).strftime('%d %b %y %H:%M:%S')}")
        print(f"{'-' * 30}")

    def display_transaction(self, transaction):
        # Display information about a specific transaction
        print(f"Transaction ID: {transaction.transaction_id}")
        if isinstance(transaction, CoinbaseTransaction):
            print("Type: Coinbase Transaction")
            print(f"Reward Amount: {transaction.amount.value} {transaction.amount.currency}")
        else:
            print(f"Sender: {transaction.sender}")
            print(f"Recipient: {transaction.recipient}")
            print(f"Amount: {transaction.amount.value} {transaction.amount.currency}")
            print(f"Transaction Type: {transaction.transaction_type}")
        print(f"{'-' * 15}")

    def create_merkle_tree(self):
        # Create a Merkle tree from the pending transactions
        merkle_tree = MerkleTree([uint256(transaction.transaction_id) for transaction in self.pending_transactions])
        return merkle_tree

    def add_block(self, block):
        # Add a new block to the chain after validating it
        if self.is_valid_block(block):
            self.db.insert_block(block)
            
            # Create and set the Merkle root for the block
            merkle_tree = self.create_merkle_tree()
            block.merkle_root = merkle_tree.get_merkle_root()

            # Append the block to the chain
            self.chain.append(block)
            return True
        else:
            print("Invalid block.")
            return False

    def is_valid_block(self, block):
        # Validate a block before adding it to the chain
        if block.index != self.chain[-1].index + 1:
            return False
        if block.previous_hash != self.chain[-1].hash:
            return False
        if not self.is_valid_proof(block):
            return False
        return True

    def is_valid_proof(self, block):
        # Check if a block's hash meets the proof of work criteria
        return block.hash.startswith('0' * blockchain_config.difficulty)

    def add_transaction(self, transaction):
        # Add a new transaction to the list of pending transactions
        self.pending_transactions.append(transaction)

    def to_serialized(self):
        # Serialize the blockchain
        return serialize(self.chain)

    @classmethod
    def from_serialized(cls, serialized_data):
        # Deserialize the blockchain
        chain = deserialize(serialized_data)
        blockchain = cls()
        blockchain.chain = chain
        return blockchain