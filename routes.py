from email import message
import json
import flask
from flask import jsonify, request
from Scrappers.scrapper import Scrapper
from __main__ import app
from skills_assets.skill_extractor import SkillExtractor


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
        data = scrapper.start_scraping(job_title=job_title, job_location=job_location)
        return jsonify(data)
    except Exception as e:
        return jsonify({"message": f"Something went wrong. {e}"})

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
        if request.method=="POST":
            text = request.get_json()['text']
        else:
            return json({"message":"request error"})

        if len(text)==0:
            return jsonify({"data":[], "message":"empty input given"})
        else:
            skill_extractor = SkillExtractor()
            skills = skill_extractor.get_skills(text)
            return jsonify({"data":skills, "message":"success"})
        
    except:
        return(
            jsonify(
                {"message":"could not etract skills, error in Skill Extractor"}
            )
        )