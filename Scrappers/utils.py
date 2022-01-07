import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from Scrappers.models import Job

ElementMap = dict()
# read from file
with open(os.path.join(os.path.dirname(__file__), "ElementMap.json"), "r") as json_file:
    ElementMap: dict = json.load(json_file)

# constants
BY: dict = {
    "ID": By.ID,
    "CLASS_NAME": By.CLASS_NAME,
    "XPATH": By.XPATH,
    "CSS_SELECTOR": By.CSS_SELECTOR,
    "TAG_NAME": By.TAG_NAME,
}

DRIVER_PATH = os.environ["DRIVER_PATH"]
options = Options()
# options.headless = True
options.set_preference("devtools.jsonview.enabled", False)
driverParams = {
    "options": options,
    "executable_path": DRIVER_PATH,
}


class FIELD(object):
    JOB_ID = "job_id"
    JOB_DESK = "job_desk"
    JOB_TITLE = "job_title"
    JOB_LOCATION = "job_location"
    JOB_LINK = "job_link"
    JOB_EMPLOYER = "job_employer"
    JOB_LOCATION = "job_location"
    JOB_SALARY = "job_salary"
    JOB_DESCRIPTION = "job_description"
    JOB_DESCRIPTION_HTML = "job_description_html"
    NA = "NA"


class JOBDESK(object):
    INDEED = "indeed"
    GLASSDOOR = "glassdoor"
    NAUKRI = "naukri"
    TIMESJOBS ="timesjobs"


# constants


def getElementMap() -> dict:
    return ElementMap


def getDriverParams():
    return driverParams


def json_to_dict(json_data: str):
    return json.loads(json_data)


def FINDELEMENT(
    element,
    child_name: str = None,
    is_list: bool = False,
    by: str = None,
    value: str = None,
):
    if child_name:
        el = ElementMap[child_name]
        if is_list:
            return element.find_elements(BY[el[0]], el[1])
        return element.find_element(BY[el[0]], el[1])
    if is_list:
        return element.find_elements(BY[by], value)
    return element.find_element(BY[by], value)


def print_result(job_data: dict):
    if not job_data.get(FIELD.JOB_DESK) or not job_data.get(FIELD.JOB_TITLE):
        print("No data found")
        return
    print({"from": job_data[FIELD.JOB_DESK], "title": job_data[FIELD.JOB_TITLE]})


def printResult(job_data: Job):
    if not job_data.DESK or not job_data.TITLE:
        print("No data found")
        return
    print({"from": job_data.DESK, "title": job_data.TITLE})
