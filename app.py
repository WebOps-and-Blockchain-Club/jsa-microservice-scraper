from flask import Flask, jsonify
from dotenv import load_dotenv
from flask import jsonify, request
import json
from skills_assets.skill_extractor import SkillExtractor
from Scrappers.models import CustomJsonEncoder
from Scrappers.scrapper import Scrapper

load_dotenv()

app = Flask(_name_)
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
        return jsonify({"message": "Something went wrong."+str(e)})


"""[summary]
@params:
    json:
        text:String

Returns:
    json: 
        data:Array
        message:String
"""


@app.route("/get-skills", methods=["GET", "POST"])
def getSkills():
    try:
        if request.method == "POST":
            text = request.get_json()['text']
        else:
            return json({"message": "request error"})

        if len(text) == 0:
            return jsonify({"data": [], "message": "empty input given"})
        else:
            skill_extractor = SkillExtractor()
            skills = skill_extractor.get_skills(text)
            return jsonify({"data": skills, "message": "success"})

    except Exception as e:
        return(
            jsonify(
                {"message": "could not etract skills, error in Skill Extractor" +
                    str(e)}
            )
        )


if _name_ == "_main_":
    app.run(debug=True, host="localhost", port=5000)