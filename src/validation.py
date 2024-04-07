# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

from config import DIFFICULTY

class Validation:
    @staticmethod
    def validate_proof_of_work(block_hash):
        # Check if the block hash meets the difficulty requirement
        return block_hash.startswith('0' * DIFFICULTY)

    @staticmethod
    def validate_genesis_block(genesis_block, Block):
        # Check if the genesis block has the correct index, previous_hash, and difficulty
        return genesis_block.index == 0 and genesis_block.previous_hash == "0" and genesis_block.hash.startswith('0' * Block.DIFFICULTY)
    
    @staticmethod
    def validate_block(block, previous_block, Block):
        # Check if the block's index is one greater than the previous block
        if block.index != previous_block.index + 1:
            return False

        # Check if the previous_hash of the new block matches the hash of the last block in the chain
        if block.previous_hash != previous_block.hash:
            return False

        # Verify the proof of work (PoW) for the new block
        if not Validation.validate_proof_of_work(block):
            return False

        # Additional validations can be added here

        return True
    
    @staticmethod
    def validate_proof_of_work(block, Block):
        # Check if the block hash meets the difficulty requirement
        return block.hash.startswith('0' * Block.DIFFICULTY)