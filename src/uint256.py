import sys

class uint256:
    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return str(self.value)

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
        return uint256(x + y)

    @staticmethod
    def subtract(x, y):
        return uint256(x - y)

    @staticmethod
    def multiply(x, y):
        return uint256(x * y)

    @staticmethod
    def divide(x, y):
        return uint256(x // y)

    @staticmethod
    def power(x, y):
        return uint256(x ** y)

    # Implement other methods similarly

    # Bloob function
    @staticmethod
    def bloob():
        return "I'm a bloob!"

    # Memset function
    @staticmethod
    def memset():
        return "I'm memset!"

# Example usage
if __name__ == "__main__":
    print(uint256.bloob())  # Output: I'm a bloob!
    print(uint256.memset())  # Output: I'm memset!
