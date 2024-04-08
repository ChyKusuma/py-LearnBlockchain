# --------------------------------------
# Created by C. Kusuma
# April 2024
# Free Software licensed under MIT
# --------------------------------------

# Warning: This codebase is for educational purposes only.
# It is not recommended for use in production environments.
# The code has not been audited and does not come with any security guarantees.
# --------------------------------------

from enum import Enum
from block import Block
from transaction import Transaction
from validation import Validation

# Define an enumeration for different phases in PBFT
class PBFTPhase(Enum):
    PREPREPARE = 0
    PREPARE = 1
    COMMIT = 2

class ConsensusAlgorithm(Enum):
    POW = 0
    PBFT = 1

class PBFTMessage:  # Define the PBFTMessage class
    def __init__(self, phase, view, block, signature):
        self.phase = phase  # PBFT phase (PREPREPARE, PREPARE, COMMIT)
        self.view = view    # View number
        self.block = block  # Block being proposed or committed
        self.signature = signature  # Signature of the message

class Consensus:
    def __init__(self, blockchain, consensus_algorithm):
        self.blockchain = blockchain
        self.consensus_algorithm = consensus_algorithm

    def mine_block(self, block):
        if self.consensus_algorithm == ConsensusAlgorithm.POW:
            return self.mine_block_with_pow(block)
        elif self.consensus_algorithm == ConsensusAlgorithm.PBFT:
            return self.mine_block_with_pbft(block)

    def mine_block_with_pow(self, block):
        # Delegate mining to pow.py
        return pow.mine_block_with_pow(block, self.blockchain.difficulty)

    def mine_block_with_pbft(self, block):
    # Validate the block using PBFT consensus logic
        if self.validate_block_with_pbft(block):
            # If the block is valid according to PBFT, return it
            return block
        else:
            # If the block is not valid according to PBFT, return None
            return None

    def validate_block_with_pbft(self, block):
        # Implement PBFT validation logic using the Validation class methods
        return Validation.validate_block(block, self.blockchain.get_last_block())

class PBFTConsensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.prepare_messages = {}  # Dictionary to store prepare messages
        self.commit_messages = {}   # Dictionary to store commit messages

    def handle_message(self, message):
        if message.phase == PBFTPhase.PREPREPARE:
            self.process_preprepare(message)
        elif message.phase == PBFTPhase.PREPARE:
            self.process_prepare(message)
        elif message.phase == PBFTPhase.COMMIT:
            self.process_commit(message)

    def process_preprepare(self, message):
        if self.validate_preprepare(message):
            self.blockchain.add_block(message.block)

    def validate_preprepare(self, message):
        # Check if the message contains all required fields
        if 'view' not in message or 'block' not in message or 'sequence_number' not in message or 'sender' not in message:
            return False
        
        # Check view number
        expected_view = self.get_expected_view()  # Implement get_expected_view() method
        if message['view'] != expected_view:
            return False
        
        # Check block integrity (assuming a function validate_block_integrity() is implemented)
        if not validate_block_integrity(message['block']):
            return False
        
        # Check sequence number
        expected_sequence_number = self.get_expected_sequence_number(message['view'])  # Implement get_expected_sequence_number() method
        if message['sequence_number'] != expected_sequence_number:
            return False
        
        # Check sender authorization (assuming a function is_sender_authorized() is implemented)
        if not is_sender_authorized(message['sender']):
            return False
        
        # All checks passed, message is valid
        return True

    def process_prepare(self, message):
        # Collect prepare messages for the block hash
        block_hash = message.block.compute_hash()
        if block_hash not in self.prepare_messages:
            self.prepare_messages[block_hash] = []
        self.prepare_messages[block_hash].append(message)

        # Check if there are enough prepare messages to move to the commit phase
        if len(self.prepare_messages[block_hash]) >= 2 * (3 * len(self.blockchain.peers) // 3) - 1:
            self.initiate_commit_phase(message.block)

    def process_commit(self, message):
        # Collect commit messages for the block hash
        block_hash = message.block.compute_hash()
        if block_hash not in self.commit_messages:
            self.commit_messages[block_hash] = []
        self.commit_messages[block_hash].append(message)

        # Check if there are enough commit messages to finalize the block commit
        if len(self.commit_messages[block_hash]) >= 2 * (3 * len(self.blockchain.peers) // 3) - 1:
            self.finalize_block_commit(message.block)

    def initiate_consensus(self, proposed_block):
        # Start the PBFT consensus process by sending a PREPREPARE message
        phase = PBFTPhase.PREPREPARE
        view = 1  # Initialize the view number
        signature = None  # Add logic to generate a signature
        preprepare_message = PBFTMessage(phase, view, proposed_block, signature)
        self.handle_message(preprepare_message)

    def initiate_commit_phase(self, block):
        # Start the commit phase by sending PREPARE messages
        phase = PBFTPhase.PREPARE
        view = 1  # Initialize the view number
        signature = None  # Add logic to generate a signature
        prepare_message = PBFTMessage(phase, view, block, signature)
        for peer in self.blockchain.peers:
            # Send prepare messages to all peers
            # Replace `peer.send(prepare_message)` with actual peer communication
            pass

    def finalize_block_commit(self, block):
        # Finalize the block commit
        self.blockchain.add_block(block)
        # Reset prepare and commit messages for this block
        block_hash = block.compute_hash()
        del self.prepare_messages[block_hash]
        del self.commit_messages[block_hash]