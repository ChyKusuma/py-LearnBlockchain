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
from block import Block
from pow import mine_block_with_pow
from consensus import ConsensusAlgorithm, PBFTConsensus
import time
from config import blockchain_config

def mine_block_and_add_to_blockchain(blockchain, consensus_algorithm):
    # Create a new block
    block_index = len(blockchain.chain)
    previous_hash = blockchain.chain[-1].hash
    block = Block(block_index, [], time.time(), previous_hash)

    # Fetch pending transactions from the mempool
    mempool = Mempool()
    pending_transactions = mempool.get_pending_transactions()

    if consensus_algorithm == ConsensusAlgorithm.POW:
        # Mine the block with Proof of Work, including pending transactions
        mined_block = mine_block_with_pow(block, blockchain_config.difficulty, "miner_address", mempool=pending_transactions)
    elif consensus_algorithm == ConsensusAlgorithm.PBFT:
        # Initiate the PBFT consensus process
        pbft_consensus = PBFTConsensus(blockchain)
        pbft_consensus.initiate_consensus(block)
        # For PBFT, the block will be added to the blockchain inside the PBFT consensus process
        mined_block = None

    # Verify mined block
    if mined_block is not None:
        # For PoW, add the mined block to the blockchain
        if consensus_algorithm == ConsensusAlgorithm.POW:
            if blockchain.add_block(mined_block):
                print("Block mined and added to the blockchain.")
            else:
                print("Failed to add the mined block to the blockchain.")
    else:
        print("Mining failed. No valid block found.")
