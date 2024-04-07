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
import hmac
import ecdsa
import base58
from Crypto.Cipher import AES
import random
import nltk

# Download NLTK word corpora (if not already downloaded)
nltk.download('words')

# Load the words corpus
words = nltk.corpus.words.words()

# Step 1: Generate key pair using ECDSA
def generate_key_pair():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key().to_string()
    hex_private_key = private_key.to_string().hex()
    hex_public_key = public_key.hex()
    return hex_private_key, hex_public_key

# Generate a passphrase with a specified number of words
def generate_passphrase(word_count):
    passphrase = ' '.join(random.choices(words, k=word_count))
    return passphrase

# Step 2: Private key encryption and decryption using passphrase
def encrypt_private_key(private_key, passphrase):
    salt = b'salt_'
    key = hashlib.pbkdf2_hmac('sha512', passphrase, salt, 1000, dklen=32)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(bytes.fromhex(private_key))
    return nonce, ciphertext, tag

def decrypt_private_key(nonce, ciphertext, tag, passphrase):
    salt = b'salt_'
    key = hashlib.pbkdf2_hmac('sha512', passphrase, salt, 1000, dklen=32)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext.hex()
    except ValueError:
        return "Decryption failed: invalid passphrase"

# Step 3: Public key hash using SHA256, hashing again using RIPEMD-160
def hash_public_key(public_key):
    hashed_public_key = hashlib.sha256(bytes.fromhex(public_key)).digest()
    ripemd160_hash = hashlib.new('ripemd160', hashed_public_key).digest()
    return ripemd160_hash

# Function to generate wallet address
def generate_wallet_address(public_key):
    # Step 3: Public key hash using SHA256, hashing again using RIPEMD-160
    hashed_public_key = hash_public_key(public_key)

    # Additional function to create a Base58 encoded address padded to 34 characters
    def add_function(input_data):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_data.encode('utf-8'))
        sha256_digest = sha256_hash.digest()

        ripemd160_hash = hashlib.new('ripemd160')
        ripemd160_hash.update(sha256_digest)
        ripemd160_digest = ripemd160_hash.digest()

        version_byte = b'\x00'
        extended_ripemd160_digest = version_byte + ripemd160_digest

        checksum = hashlib.sha256(hashlib.sha256(extended_ripemd160_digest).digest()).digest()[:4]

        address_with_checksum = extended_ripemd160_digest + checksum

        # Generate Base58 encoded address
        hash_base58check = base58.b58encode(address_with_checksum).decode('utf-8')

        # Pad the address to 34 characters
        padded_address = hash_base58check.ljust(34, '1')

        return padded_address

    # Generate Base58 encoded address padded to 34 characters
    encoded_public_key_hash = add_function(hashed_public_key.hex())
    return encoded_public_key_hash

if __name__ == "__main__":
    # Generate passphrase using NLTK
    passphrase = generate_passphrase(6)  # Generate a passphrase with 6 words
    print("Passphrase:", passphrase)

    # Step 1: Generate key pair
    hex_private_key, hex_public_key = generate_key_pair()
    print("\nGenerated Key Pair:")
    print("Private key:", hex_private_key)
    print("Public key:", hex_public_key)

    passphrase_bytes = passphrase.encode()

    # Step 2: Private key encryption and decryption using passphrase
    nonce, ciphertext, tag = encrypt_private_key(hex_private_key, passphrase_bytes)
    print("\nEncrypted Private Key:")
    print("Nonce:", nonce.hex())
    print("Ciphertext:", ciphertext.hex())
    print("Tag:", tag.hex())
    decrypted_private_key = decrypt_private_key(nonce, ciphertext, tag, passphrase_bytes)
    print("\nDecrypted Private Key:", decrypted_private_key)

    # Step 3: Public key hash using SHA256, hashing again using RIPEMD-160
    hashed_public_key = hash_public_key(hex_public_key)
    print("\nPublic Key Hash (RIPEMD-160):", hashed_public_key.hex())

    # Generate wallet address
    wallet_address = generate_wallet_address(hex_public_key)
    print("\nWallet Address:", wallet_address)