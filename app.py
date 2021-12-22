from flask import Flask, jsonify
import flask
import pymongo
from pymongo import MongoClient
from scraper import scraping
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


@app.route('/')
def ping_server():
    return "Server is running now!"

    """[summary]
    @params:
        job: string
        location: string

    Returns:
        array: An array of job listing
    """


@app.route('/job-search', methods=['POST'])
def jobsearch():

    data = scraping()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
