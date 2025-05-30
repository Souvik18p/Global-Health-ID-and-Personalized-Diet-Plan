from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from Blockchain_module import Blockchain  # your blockchain code here
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # allows cross-origin requests from your frontend

# Mongo setup
client = MongoClient("mongodb+srv://souvikpramanick018:a0oUaw6JFpT3iNXn@cluster0.98trv.mongodb.net/blockchain?retryWrites=true&w=majority")
collection = client["blockchain"]["Blocks"]

blockchain = Blockchain()

@app.route('/create_block', methods=['POST'])
def create_block():
    data = request.json
    blockchain.add_block(data)
    blockchain.save_block_to_db(blockchain.get_latest_block(), collection)
    return jsonify({"message": "Block added successfully", "block": data}), 201

@app.route('/get_block', methods=['GET'])
def get_block():
    patient_id = request.args.get("patient_id")
    block = blockchain.get_block_from_db(patient_id, collection)
    if block:
        return jsonify(block), 200
    else:
        return jsonify({"error": "Block not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
