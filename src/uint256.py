# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

import sys
from decimal import Decimal
from tiny import TinyUint256  # Import TinyUint256 from tiny.py

class uint256:
    WORD_SIZE_BYTES = 32
    WORD_SIZE_BITS = WORD_SIZE_BYTES * 8

    def __init__(self, value=0):
        if isinstance(value, str):
            # Convert hexadecimal string to int
            self.value = int(value, 16)
        elif isinstance(value, bytes):
            # Convert bytes to int
            self.value = int.from_bytes(value, byteorder='big')
        elif isinstance(value, TinyUint256):  # Check if value is a TinyUint256 object
            self.value = value.value
        else:
            self.value = int(value)

        # Ensure that the value is within the range of a 256-bit unsigned integer
        if not 0 <= self.value < 2 ** 256:
            raise ValueError("Value out of range for uint256")

    def __str__(self):
        return hex(self.value)

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    @staticmethod
    def bytes_to_int(byte_array):
        return int.from_bytes(byte_array, byteorder='big')

    @staticmethod
    def int_to_bytes(integer):
        return integer.to_bytes(uint256.WORD_SIZE_BYTES, byteorder='big')

    @staticmethod
    def int_to_binary_string(integer):
        return bin(integer)[2:].zfill(uint256.WORD_SIZE_BITS)

    @staticmethod
    def add(x, y):
        # Convert x and y to uint256 objects if they are TinyUint256 objects
        if isinstance(x, TinyUint256):
            x = uint256(x.value)
        if isinstance(y, TinyUint256):
            y = uint256(y.value)
        result = x.value + y.value
        if result >= 2 ** 256:
            raise OverflowError("Addition result exceeds 256 bits")
        return uint256(result)

    @staticmethod
    def subtract(x, y):
        if x.value < y.value:
            raise ValueError("Subtraction result cannot be negative")
        return uint256(x.value - y.value)

    @staticmethod
    def multiply(x, y):
        result = x.value * y.value
        if result >= 2 ** 256:
            raise OverflowError("Multiplication result exceeds 256 bits")
        return uint256(result)

    @staticmethod
    def divide(x, y):
        if y.value == 0:
            raise ZeroDivisionError("Division by zero")
        return uint256(x.value // y.value)

    @staticmethod
    def power(x, y):
        result = x.value ** y.value
        if result >= 2 ** 256:
            raise OverflowError("Power result exceeds 256 bits")
        return uint256(result)

    @staticmethod
    def bits_to_bytes(bits):
        return bits // 8

    @staticmethod
    def bytes_to_bits(bytes_):
        return bytes_ * 8

    # Bloom function
    @staticmethod
    def bloom():
        return "I'm a bloom!"

    # Memset function
    @staticmethod
    def memset():
        return "memset!"

    # Conversion function to TinyUint256
    def to_tiny_uint256(self):
        return TinyUint256.memset()

    # Additional algebraic operations
    def square(self):
        return self.multiply(self)

    def cube(self):
        return self.multiply(self).multiply(self)

    def square_root(self):
        return uint256(int(self.value ** 0.5))

    def cube_root(self):
        return uint256(int(self.value ** (1 / 3)))

    def modulus(self, n):
        return uint256(self.value % n)

    def factorial(self):
        result = 1
        for i in range(2, self.value + 1):
            result *= i
            if result >= 2 ** 256:
                raise OverflowError("Factorial result exceeds 256 bits")
        return uint256(result)

    def exponent(self, exp):
        result = self.value ** exp
        if result >= 2 ** 256:
            raise OverflowError("Exponentiation result exceeds 256 bits")
        return uint256(result)