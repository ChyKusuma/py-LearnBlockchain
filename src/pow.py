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
import struct
from serialized import serialize
from uint256 import uint256
from validation import Validation

def bytes_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder='big')

def mine_block_with_pow(block, target_bits):
    while True:
        block.nonce += 1
        block.hash = block.compute_hash()
        if Validation.validate_proof_of_work(block.hash):  # Use Validation class to validate proof of work
            return block

def is_valid_proof(block, target_bits):
    block_header_serialized = block.serialize()  # Serialize the entire block
    block_hash = hashlib.sha256(hashlib.sha256(block_header_serialized).digest()).digest()
    block_hash_int = uint256(bytes_to_int(block_hash))
    target = uint256(1 << (256 - target_bits))
    return block_hash_int < target

def calculate_target(bits):
    exponent = bits >> 24
    mantissa = bits & 0x7fffff
    target_hexstr = '%064x' % (mantissa * (1 << (8 * (exponent - 3))))
    return bytes.fromhex(target_hexstr)

def bits_to_target(bits):
    return uint256(bytes_to_int(calculate_target(bits)))

