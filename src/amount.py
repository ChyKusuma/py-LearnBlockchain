# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

class Amount:
    def __init__(self, value, currency):
        self.value = value
        self.currency = currency

    def to_obj(self):
        return {
            "value": self.value,
            "currency": self.currency
        }
    
    # Define the total amount of the asset as coinbase
    COINBASE_AMOUNT = 30000000

    # Define the mining reward
    MINING_REWARD = 10  # For example, set the mining reward to 10 units of the asset

    @staticmethod
    def from_obj(data):
        return Amount(data['value'], data['currency'])

    @staticmethod
    def get_coinbase_amount():
        # This method should return the coinbase amount as an Amount object
        return Amount(10, "COINS")  # Example values

    @staticmethod
    def get_mining_reward():
        # This method should return the mining reward amount as a simple integer
        return 10  # Example value