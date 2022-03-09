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

DRIVER_PATH = 'D:\driver\geckodriver.exe'
options = Options()
# options.headless = True
options.set_preference("devtools.jsonview.enabled", False)
driverParams = {
    "options": options,
    "executable_path": DRIVER_PATH,
}


def getElementMap():
    return ElementMap


def getDriverParams():
    return driverParams


def tryCloseDreiver(driver):
    try:
        driver.close()
    except:
        pass


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


def printResult(job_data: Job):
    if not job_data.DESK or not job_data.TITLE:
        print("No data found")
        return
    print({"from": job_data.DESK, "title": job_data.TITLE})
