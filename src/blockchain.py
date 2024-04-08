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

class Blockchain:
    def __init__(self, db):
        self.chain = []
        self.pending_transactions = []
        self.db = db  # Database instance

        # Create the genesis block
        self.create_genesis_block()

    def create_genesis_block(self):
        # Manually create the genesis block with index 0 and previous hash "0"
        genesis_block = Block(0, [])  # Remove the timestamp argument as it's generated automatically
        # Set the genesis block data from config
        genesis_block.data = blockchain_config.genesis_block_data
        # Mine the genesis block
        genesis_block.mine_block()
        # Append the mined genesis block to the chain
        self.chain.append(genesis_block)

    def display_chain(self):
        # Display the entire blockchain
        for block in self.chain:
            print("Block Index:", block.index)
            print("Previous Hash:", block.previous_hash)
            print("Hash:", block.hash)
            print("Transactions:")

            # Print block header
            print("Block Header:")
            for key, value in block.block_header.items():
                print(f"{key}: {value}")

            print("---------------")

    def mine_block(self):
        # Get the current timestamp
        timestamp = time.time()
        timestamp_str = datetime.utcfromtimestamp(timestamp).strftime('%d %b %y %H:%M:%S')  # Format the timestamp

        # Check if the chain is empty, indicating the genesis block
        if len(self.chain) == 0:
            # Create a new block with index 0 and no previous hash for the genesis block
            new_block = Block(0, self.pending_transactions, timestamp, "")
        else:
            # Get the index of the last block
            index = self.chain[-1].index + 1
            # Get the hash of the last block
            previous_hash = self.chain[-1].hash
            # Create a new block with the pending transactions and current timestamp
            new_block = Block(index, self.pending_transactions, timestamp, previous_hash)

        print("Mining block with index:", new_block.index, flush=True)  # Print the index of the block being mined
        print("Mining block with timestamp:", timestamp_str, flush=True)  # Print the timestamp in the desired format
        print("Mining block...", flush=True)

        # Mine the block
        hash_attempts = []  # List to store hash attempts
        attempt_count = 1
        while True:
            new_block.hash = new_block.compute_hash()  # Update the hash after mining
            
            # Append the hash attempt to the list
            hash_attempts.append(new_block.hash)

            print(f"Attempt {attempt_count}: Hash Result: {new_block.hash}", flush=True)  # Print the current hash attempt

            # Check if the hash meets the difficulty requirement
            if new_block.hash.startswith('0' * blockchain_config.difficulty):  # Use blockchain_config.difficulty
                print("Block mined successfully!", flush=True)
                break  # Exit the loop if a valid hash is found
            else:
                # Increment nonce and continue mining
                new_block.nonce += 1
                attempt_count += 1

        # Append the mined block to the chain
        self.chain.append(new_block)

        # Clear the list of pending transactions
        self.pending_transactions = []

    def create_merkle_tree(self):
        # Construct a Merkle tree for the pending transactions
        merkle_tree = MerkleTree([uint256(transaction.transaction_id) for transaction in self.pending_transactions])
        return merkle_tree

    def add_block(self, block):
        if self.is_valid_block(block):
            # Save block details into the database
            self.db.insert_block(block)
            
            # Compute the Merkle root for the block's transactions
            merkle_tree = self.create_merkle_tree()
            block.merkle_root = merkle_tree.get_merkle_root()

            # Print block header information
            print("Block Header Information:")
            print("Index:", block.index)
            print("Timestamp:", block.timestamp)
            print("Previous Hash:", block.previous_hash)
            print("Nonce:", block.nonce)
            print("Hash:", block.hash)
            print("Merkle Root:", block.merkle_root)

            # Append the block to the chain
            self.chain.append(block)
            return True
        else:
            print("Invalid block. Reason:")
            if block.index != self.chain[-1].index + 1:
                print("Invalid index.")
            elif block.previous_hash != self.chain[-1].hash:
                print("Invalid previous hash.")
            elif not self.is_valid_proof(block):
                print("Invalid proof of work.")
            return False
        
    def is_valid_block(self, block):
        # Check if the block's index is one greater than the previous block
        if block.index != self.chain[-1].index + 1:
            return False

        # Check if the previous_hash of the new block matches the hash of the last block in the chain
        if block.previous_hash != self.chain[-1].hash:
            return False

        # Verify the proof of work (PoW) for the new block
        if not self.is_valid_proof(block):
            return False

        # Additional validations can be added here
        return True

    def is_valid_proof(self, block):
        # Check if the block hash meets the difficulty requirement
        return block.hash.startswith('0' * blockchain_config.difficulty)

    def mine_pending_transactions(self):
        # Create a new block with the pending transactions and mine it
        new_block = Block(len(self.chain), self.pending_transactions, time.time(), self.chain[-1].hash)
        new_block.mine_block(blockchain_config.difficulty)  # Mine the block with PoW using blockchain_config.difficulty
        self.chain.append(new_block)

        # Clear the list of pending transactions
        self.pending_transactions = []

    def add_transaction(self, transaction):
        # Add a transaction to the list of pending transactions
        self.pending_transactions.append(transaction)

    def to_serialized(self):
        # Serialize the blockchain using the serialize function
        return serialize(self.chain)

    @classmethod
    def from_serialized(cls, serialized_data):
        # Deserialize the blockchain using the deserialize function
        chain = deserialize(serialized_data)
        blockchain = cls()
        blockchain.chain = chain
        return blockchain