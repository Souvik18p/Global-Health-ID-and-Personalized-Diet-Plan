# app/Blockchain_module.py

import hashlib
import time
import random
import string
from pymongo import MongoClient

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]
    
    def get_block_from_db(self, patient_id, collection):
        """Retrieve a block by Patient ID from MongoDB."""
        return collection.find_one({"data.Patient ID": patient_id})

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), latest_block.hash, time.time(), data)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block

def generate_patient_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def get_mongo_client():
    db_uri = "mongodb+srv://souvikpramanick018:a0oUaw6JFpT3iNXn@cluster0.98trv.mongodb.net/blockchain?retryWrites=true&w=majority"
    client = MongoClient(db_uri)
    db = client["blockchain"]
    collection = db["Blocks"]
    return collection

def create_health_id(data):
    collection = get_mongo_client()
    blockchain = Blockchain()
    
    patient_id = generate_patient_id()
    data["Patient ID"] = patient_id

    new_block = blockchain.add_block(data)

    # Save to MongoDB
    block_data = {
        "index": new_block.index,
        "previous_hash": new_block.previous_hash,
        "timestamp": new_block.timestamp,
        "data": new_block.data,
        "nonce": new_block.nonce,
        "hash": new_block.hash
    }
    collection.insert_one(block_data)

    return patient_id, new_block.previous_hash, new_block.hash

my_blockchain = Blockchain()

def search_patient_by_id(patient_id):
    db_uri = "mongodb+srv://souvikpramanick018:a0oUaw6JFpT3iNXn@cluster0.98trv.mongodb.net/blockchain?retryWrites=true&w=majority"
    client = MongoClient(db_uri)
    db = client["blockchain"]
    collection = db["Blocks"]

    record = my_blockchain.get_block_from_db(patient_id, collection)

    if record:
        data = record.get("data", {})
        return {
            "patient_id": data.get("Patient ID"),
            "hospital": data.get("Hospital"),
            "doctor": data.get("Doctor"),
            "patient_name": data.get("Patient Name"),
            "age": data.get("Age"),
            "weight": data.get("Weight"),
            "height": data.get("Height"),
            "issues": data.get("Issues"),
            "suggestions": data.get("Suggestions"),
        }
    else:
        return None