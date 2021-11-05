from flask import Flask, jsonify
import flask
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def ping_server():
    return "CFI WebOps!"

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)