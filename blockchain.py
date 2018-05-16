import hashlib
import json
from time import time
from uuid import uuid4
from textwrap import dedent
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests
import rsa

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        # this is the first block in the blockchain
        self.new_block(previous_hash=1, proof=100)


    ############################################################
    # Create a new Block in the Blockchain
    # @param proof - the number that solved the PoW algorithm
    # @param previous_hash - the hash of the previous block
    # @return - the new block for the chain
    ############################################################
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block


    ###################################################################
    # Creates a new transaction to go into the next mined Block
    # @param sender - the person who is initiating the transaction
    # @param recipient - the person who is receiving the amount
    # @param amount - the amount to send in the transaction
    # @return - the index of the block that will hold this transaction
    ###################################################################
    def new_transaction(self, sender, recipient, amount):
        #generate a new key pair for each transaction -- iffy...
        (pub, priv) = rsa.newkeys(512)

        # create the message to sign
        message = sender + recipient + str(amount)
        message = message.encode('utf8')

        # sign the contents of the message
        sig = rsa.sign(message, priv, 'SHA-1')
        signature = str(sig)

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'signature': signature,
        })
        return self.last_block['index'] + 1


    @property
    def last_block(self):
        return self.chain[-1]


    ################################################
    # Creates a SHA-256 hash of a Block
    # @param block - the block that is to be hashed
    # @return - sha256 hex digest of the the block
    ################################################
    @staticmethod
    def hash(block):
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    ##################################################
    # solves the proof of work algorithm
    # @param last_block - the last block
    # @return - the integer that solved the algorithm
    ##################################################
    def proof_of_work(self, last_block):
        # this is where we can be creative with how hard we want it to be to
        # mine new blocks
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof


    ####################################################
    # checks if the proof solves the PoW algorithm
    # @param last_proof - the previous proof
    # @param proof - the current proof
    # @param last_hash - the hash of the previous block
    # @return - true if valid, false otherwise
    ####################################################
    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        # this is where we can be creative with how hard we want it to be to
        # mine new blocks

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


    ###########################################################
    # add a new node to the list of nodes
    # @param address - the web address of the node to register
    ###########################################################
    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


    #############################################################
    # determine if the blockchain is valid
    # @param chain - the chain whose validity is in question
    # @return - True if we have the valid chain, false otherwise
    #############################################################
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n---------\n")

            last_block_hash = self.hash(last_block)
            # check that the hash of the block is correct
            if block['previous_hash'] != last_block_hash:
                return False

            # check that the PoW is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1
        return True


    #############################################################
    # sets the chain to the longest chain in the network
    # @return - True if our chain was replaced, false otherwise
    #############################################################
    def resolve_conflicts(self):
        neighbors = self.nodes
        new_chain = None

        # we are looking for a longer chain
        max_length = len(self.chain)

        # fetch and verify all the chains in the network
        for node in neighbors:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

                # replace the chain if we found the new longer chain
                if new_chain:
                    self.chain = new_chain
                    return True

                return False



# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

# the endpoint used to mine a block
@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # load the private key for the miner
    #with open('priv1.pem', mode='rb') as privateFile:
    #    keyData = privateFile.read()
    #privkey = rsa.PrivateKey.load_pkcs1(keyData)
    #priv_key = str(privkey)
    # create a signature
    #message = 0 + node_identifier + 1
    #signature = rsa.sign(message, privkey, 'SHA-1')

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# the endpoint for creation of a new transaction
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

# the endpoint to fetch the whole blockchain
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

# the endpoint to register a new node
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

# the endpoint to resolve chain confliction
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


# check for a port variable to simulate multiple users/nodes
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
