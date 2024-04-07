# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------


from validation import Validation

class Mempool:
    def __init__(self):
        self.pending_transactions = []

    def add_transaction_request(self, transaction_request):
        """
        Add a transaction request to the mempool.
        Transaction requests are not validated yet.
        """
        self.pending_transactions.append(transaction_request)

    def validate_transaction(self, transaction, block_hash, difficulty):
        """
        Validate a transaction.
        You can implement your validation logic here.
        For example, checking for double spending or verifying signatures.
        """
        # Use the validate_proof_of_work method from validation.py to validate the transaction
        return Validation.validate_proof_of_work(transaction, block_hash, difficulty)

    def process_pending_transactions(self, block_hash, difficulty):
        """
        Process pending transactions and move valid transactions to the mempool.
        """
        valid_transactions = []
        for transaction in self.pending_transactions:
            if self.validate_transaction(transaction, block_hash, difficulty):
                valid_transactions.append(transaction)
            else:
                print(f"Invalid transaction: {transaction}")
        
        # Remove processed transactions from pending transactions
        self.pending_transactions = [
            tx for tx in self.pending_transactions if tx not in valid_transactions
        ]
        
        return valid_transactions

    def get_pending_transactions(self):
        """
        Get all pending transactions in the mempool.
        """
        return self.pending_transactions