from flask import Flask, jsonify
from dotenv import load_dotenv
import flask
from Scrappers.models import CustomJsonEncoder
from Scrappers.scrapper import Scrapper

load_dotenv()

app = Flask(__name__)
app.json_encoder = CustomJsonEncoder


scrapper = Scrapper()


@app.route("/")
def ping_server():
    return "Server is running now!"


"""[summary]
@params:
    job: string
    location: string
Returns:
    array: An array of job listing
"""


@app.route("/job-search", methods=["GET"])
def jobSearch():
    try:
        job_title = flask.request.args.get("job_title")
        job_location = flask.request.args.get("job_location")
        if not job_title or not job_location:
            raise Exception("Invalid input")
    except:
        return (
            jsonify(
                {"message": "Please provide job_title and job_location in query params"}
            ),
            400,
        )
    try:
        data = scrapper.start_scraping(
            job_title=job_title, job_location=job_location)
        return jsonify(data)
    except Exception as e:
        return jsonify({"message": f"Something went wrong. {e}"})


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)
