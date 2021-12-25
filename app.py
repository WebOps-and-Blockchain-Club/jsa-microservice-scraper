from flask import Flask, jsonify
import flask
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

import routes

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
