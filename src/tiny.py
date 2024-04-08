# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

class TinyUint256:
    MAX_VALUE = 2 ** 256 - 1

    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return hex(self.value)

    @staticmethod
    def add(x, y):
        result = x + y
        if result > TinyUint256.MAX_VALUE:
            raise OverflowError("Addition result exceeds 256 bits")
        return TinyUint256(result)

    @staticmethod
    def subtract(x, y):
        if x < y:
            raise ValueError("Subtraction result cannot be negative")
        return TinyUint256(x - y)

    @staticmethod
    def multiply(x, y):
        result = x * y
        if result > TinyUint256.MAX_VALUE:
            raise OverflowError("Multiplication result exceeds 256 bits")
        return TinyUint256(result)

    # Conversion function to uint256
    def to_uint256(self):
        try:
            from uint256 import uint256  # Import uint256 class here to avoid circular import
            return uint256(self.value)
        except ImportError:
            # Handle ImportError if uint256 class is not available
            raise ImportError("uint256 class not found")

    @staticmethod
    def memset():
        return "memset!"