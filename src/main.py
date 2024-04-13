# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

from db import Database
from block import Block
from transaction import CoinbaseTransaction
from account import Account
from amount import Amount
from blockchain import Blockchain  # Import the Blockchain class

if __name__ == "__main__":
    # Create a database object
    db = Database('wallets.db')  # Adjust the database name as needed

    # Generate core developer's account data
    core_dev_passphrase = "muckerism undesirousness semipyramidal amimide chaulmoograte glyphography"
    core_dev_public_key_hash = "4ea81a7c6763cfbd6f3a226e60beb3caa1d7b07a"
    core_dev_wallet_address = "1CD5YecosxDEKihsr4ZXvrPghWymx4C9PX"

    # Print core developer's information
    print("Core Developer's Public Key Hash:", core_dev_public_key_hash)
    print("Core Developer's Wallet Address:", core_dev_wallet_address)

    # Create a blockchain instance
    blockchain = Blockchain(db)

    # Creating a miner reward transaction for the genesis block
    miner_reward = CoinbaseTransaction(core_dev_wallet_address, Amount(10, "COINS"))  # Create a CoinbaseTransaction object

    # Append the miner reward transaction to the pending transactions
    blockchain.add_transaction(miner_reward)

    # Mine the pending transactions to create the genesis block
    blockchain.mine_pending_transactions()

    # Check if the core developer's wallet address already exists in the database
    core_dev_exists = db.check_account_exists(core_dev_wallet_address)

    if not core_dev_exists:
        # Create an Account object for the core developer
        core_dev_account = Account(core_dev_passphrase, core_dev_public_key_hash, core_dev_wallet_address, miner_reward.amount, account_type="core-developer")
        # Insert the core developer's account data into the database
        db.insert_account(core_dev_account)
        print("Core Developer account created and inserted into the database.")
    else:
        print("Core Developer account already exists in the database.")

    # Call the display_chain method to print the blockchain information
    blockchain.display_chain()

    # Mine the next block
    next_block = Block(len(blockchain.chain), [], blockchain.chain[-1].hash)
    blockchain.mine_block(next_block)

    # Call the display_chain method again to print the updated blockchain information
    blockchain.display_chain()

    # Close the database connection (no longer necessary as handled by the Database class)
    db.close()