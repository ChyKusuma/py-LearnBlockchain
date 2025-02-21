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
from uint256 import uint256

class MerkleTree:
    def __init__(self, transaction_ids):
        self.transaction_ids = [uint256(tx_id) for tx_id in transaction_ids]
        self.merkle_root = self.compute_merkle_root()

    def compute_merkle_root(self):
        if len(self.transaction_ids) == 0:
            return self.compute_empty_hash()
        if len(self.transaction_ids) == 1:
            return self.transaction_ids[0]

        # List to store intermediate hash values
        intermediate_hashes = [tx_id.value for tx_id in self.transaction_ids]

        while len(intermediate_hashes) > 1:
            # If the number of hashes is odd, duplicate the last hash
            if len(intermediate_hashes) % 2 != 0:
                intermediate_hashes.append(intermediate_hashes[-1])

            # Pair adjacent hashes and hash them together
            paired_hashes = [b''.join(intermediate_hashes[i:i+2]) for i in range(0, len(intermediate_hashes), 2)]
            intermediate_hashes = [uint256(hashlib.sha256(pair).digest()) for pair in paired_hashes]

        return intermediate_hashes[0]

    def get_merkle_root(self):
        return self.merkle_root

    @staticmethod
    def compute_block_merkle_root(transactions):
        # Extract transaction IDs from transactions
        transaction_ids = [transaction.transaction_id for transaction in transactions]

        # Handle special cases
        if len(transaction_ids) == 0:
            return hashlib.sha256(b'').hexdigest()  # Empty hash
        elif len(transaction_ids) == 1:
            return transaction_ids[0]  # Single transaction hash
        else:
            # Compute the Merkle root for the block using the transaction IDs
            merkle_tree = MerkleTree(transaction_ids)
            return merkle_tree.get_merkle_root()

    @staticmethod
    def compute_empty_hash():
        return hashlib.sha256(b'').hexdigest()  # Empty hash

    @staticmethod
    def compute_uncle_hash():
        return hashlib.sha256(b'uncle').hexdigest()  # Uncle hash

    @staticmethod
    def compute_child_hash():
        return hashlib.sha256(b'child').hexdigest()  # Child hash