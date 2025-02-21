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
from amount import Amount
import mempool
from serialized import serialize, deserialize

class Transaction:
    def __init__(self, sender, recipient, amount, transaction_type=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.transaction_id = self.compute_transaction_id()  # Generate transaction ID
        self.transaction_type = transaction_type  # Include transaction type attribute

    def compute_transaction_id(self):
        # Generate a unique transaction ID using sender, recipient, and amount
        return hashlib.sha256((self.sender + self.recipient + str(self.amount.value) + self.amount.currency).encode()).hexdigest()

    def to_obj(self):
        # Serialize the object directly
        return serialize({
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount.to_obj(),  # Serialize the amount object
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type  # Serialize transaction type
        })

    @staticmethod
    def from_obj(data):
        sender = data['sender']
        recipient = data['recipient']
        amount = Amount.from_obj(data['amount'])  # Deserialize the amount object
        transaction_type = data.get('transaction_type')  # Retrieve transaction type if available
        return Transaction(sender, recipient, amount, transaction_type)

    def broadcast_to_mempool(self):
        # Add the transaction request to the mempool
        mempool_instance = mempool.Mempool()
        mempool_instance.add_transaction_request(self)

    def serialize(self):
        return self.to_obj()  # Use the modified to_obj method

    @staticmethod
    def deserialize(serialized_data):
        data = deserialize(serialized_data)
        amount = Amount.from_obj(data['amount'])
        transaction_type = data.get('transaction_type')  # Retrieve transaction type if available
        return Transaction(data['sender'], data['recipient'], amount, transaction_type)

class CoinbaseTransaction:
    def __init__(self, recipient, amount):
        self.recipient = recipient
        self.amount = amount  # Make sure 'amount' is an instance of the 'Amount' class
        self.transaction_id = self.compute_transaction_id()

    def compute_transaction_id(self):
        # Generate a unique transaction ID using recipient and amount
        return hashlib.sha256((self.recipient + str(self.amount.value) + self.amount.currency).encode()).hexdigest()

    def to_obj(self):
        return {
            "recipient": self.recipient,
            "amount": self.amount.to_obj(),
            "transaction_id": self.transaction_id
        }

    @staticmethod
    def from_obj(data):
        recipient = data['recipient']
        amount = Amount.from_obj(data['amount'])
        return CoinbaseTransaction(recipient, amount)

    def serialize(self):
        return serialize(self.to_obj())

    @staticmethod
    def deserialize(serialized_data):
        data = deserialize(serialized_data)
        amount = Amount.from_obj(data['amount'])
        return CoinbaseTransaction(data['recipient'], amount)
