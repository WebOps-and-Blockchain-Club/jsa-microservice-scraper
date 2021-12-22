import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

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

DRIVER_PATH = "D:\driver\geckodriver.exe"
options = Options()
options.headless = True
driverParams = {
    "options": options,
    "executable_path": DRIVER_PATH,
}

# constants


def getElementMap() -> dict:
    return ElementMap


def getDriverParams():
    return driverParams


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
    if not job_data["from"] or not job_data["title"]:
        return
    print({"from": job_data.get("from"), "title": job_data.get("title")})
