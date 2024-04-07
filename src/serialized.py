# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

import pickle

# Serialize an object
def serialize(obj):
    return pickle.dumps(obj)

# Deserialize an object
def deserialize(serialized_data):
    return pickle.loads(serialized_data)