# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

from crypter import generate_passphrase, generate_key_pair, hash_public_key, generate_wallet_address
from account import Account
from db import Database

if __name__ == "__main__":
    # Generate passphrase using NLTK
    passphrase = generate_passphrase(6)
    print("Passphrase:", passphrase)

    # Step 1: Generate key pair
    _, hex_public_key = generate_key_pair()

    # Step 3: Public key hash using SHA256, hashing again using RIPEMD-160
    hashed_public_key = hash_public_key(hex_public_key)
    print("Public Key Hash (RIPEMD-160):", hashed_public_key.hex())

    # Generate wallet address
    wallet_address = generate_wallet_address(hex_public_key)
    print("Wallet Address:", wallet_address)

    # Create a database object
    db = Database('wallets.db')

    # Create an account object
    account = Account(db, passphrase, hashed_public_key.hex(), wallet_address)

    # Insert account data into the database
    account.save_to_database()

    # Close the database connection
    db.close()