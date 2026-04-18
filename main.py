from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block['proof'])
    previous_hash = blockchain.hash(previous_block)

    blockchain.add_transaction(sender="system", receiver="you", amount=1)

    block = blockchain.create_block(proof, previous_hash)

    return jsonify({
        'message': 'Block mined!',
        'block': block
    }), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json_data = request.get_json()
    required = ['sender', 'receiver', 'amount']

    if not all(k in json_data for k in required):
        return 'Missing values', 400

    index = blockchain.add_transaction(
        json_data['sender'],
        json_data['receiver'],
        json_data['amount']
    )

    return jsonify({'message': f'Transaction will be added to Block {index}'}), 201

@app.route('/is_valid', methods=['GET'])
def is_valid():
    valid = blockchain.is_chain_valid(blockchain.chain)

    return jsonify({
        'message': 'Valid blockchain' if valid else 'Invalid blockchain'
    }), 200

if __name__ == '__main__':
    app.run(debug=True)