# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

class BlockchainConfig:
    def __init__(self):
        # Default configuration values
        self.difficulty = 4
        self.block_reward = 10  # Reward for mining a block
        self.max_block_size = 1024  # Maximum size of a block in bytes
        self.block_interval = 10  # Time interval between blocks in seconds
        self.genesis_block_data = "Genesis Block"  # Data for the genesis block
        self.genesis_block_index = 0  # Index of the genesis block
        self.genesis_block_previous_hash = "0"  # Previous hash of the genesis block

# Singleton pattern to ensure there's only one configuration instance
blockchain_config = BlockchainConfig()