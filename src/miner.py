# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

from mempool import Mempool
from pow import mine_block_with_pow
from block import Block
from blockchain import Blockchain  # Import the Blockchain class
import time
from config import blockchain_config

def mine_block_and_add_to_blockchain(blockchain):
    # Create a new block
    block_index = len(blockchain.chain)
    previous_hash = blockchain.chain[-1].hash
    block = Block(block_index, [], time.time(), previous_hash)

    # Fetch pending transactions from the mempool
    mempool = Mempool()
    pending_transactions = mempool.get_pending_transactions()

    # Mine the block with Proof of Work, including pending transactions
    mined_block = mine_block_with_pow(block, blockchain_config.difficulty, "miner_address", mempool=pending_transactions)

    # Verify mined block
    if mined_block is not None:
        # Add the mined block to the blockchain
        if blockchain.add_block(mined_block):
            print("Block mined and added to the blockchain.")
        else:
            print("Failed to add the mined block to the blockchain.")
    else:
        print("Mining failed. No valid block found.")

if __name__ == "__main__":
    # Initialize blockchain
    blockchain = Blockchain()

    # Mine a block and add it to the blockchain
    mine_block_and_add_to_blockchain(blockchain)