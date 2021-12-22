import ray
import time
from typing import Callable
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import utils as ut


@ray.remote
def start_scraping_glassdoor(
    job_location,
    job_title,
    callbackFn: Callable[[dict], None] = None,
    utils=ut,
):
    print("Starting scraping glassdoor")
    driverParams = utils.getDriverParams()
    driver = webdriver.Firefox(**driverParams)
    driver.maximize_window()
    driver.delete_all_cookies()

    locationIDLink = f"https://www.glassdoor.co.in/util/ajax/findLocationsByFullText.htm?locationSearchString={job_location}&allowPostalCodes=true"

    driver.get(locationIDLink)

    jsonRes = utils.FINDELEMENT(driver, "GD_jsonRes").text
    jsonRes = json.loads(jsonRes)
    jsonRes

    locDet = jsonRes["locations"][0]
    locID = str(locDet["id"])
    locType = locDet["type"]

    link = (
        "https://www.glassdoor.co.in/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="
        + "-".join(job_title.split(" "))
        + "&typedLocation="
        + "-".join(job_location.split(" "))
        + "&locT="
        + locType
        + "&locId="
        + locID
        + "&jobType=&context=Jobs&sc.keyword="
        + "+".join(job_title.split(" "))
        + "&dropdown=0"
    )

    driver.get(link)

    def try_close_popup():
        try:
            modalCloseButton = utils.FINDELEMENT(driver, "GD_modalCloseButton")
            modalCloseButton.click()
            time.sleep(0.1)
        except:
            pass

    try_close_popup()
    # scrape job list
    jobDetailsList = []
    dataset = utils.FINDELEMENT(driver, "GD_jobListPath")
    datasetList = utils.FINDELEMENT(dataset, "GD_datasetList", is_list=True)
    for jobCard in datasetList:
        try:
            jobCard.click()
        except:
            time.sleep(0.1)
            continue
        try_close_popup()
        jobDetails = {"from": "glassdoor"}
        count = 0
        try:
            anchor = utils.FINDELEMENT(jobCard, "GD_jobLink")
            anchor.get_attribute("href")
            jobDetails["job_link"] = anchor.get_attribute("href")
        except:
            jobDetails["job_link"] = "NA"
        while True:
            count += 1
            time.sleep(0.1)
            try:
                AllDetailsBox = utils.FINDELEMENT(driver, "GD_DetailsBoxID")
                OverViewBox = utils.FINDELEMENT(AllDetailsBox, "GD_OverViewBoxClass")
                Title = utils.FINDELEMENT(OverViewBox, "GD_TitleClassName").text
                jobDetails["title"] = Title
                DescriptionBox = utils.FINDELEMENT(driver, "GD_DescriptionBoxId")
                count = 10
                #
                #
                try:
                    KeyProp = utils.FINDELEMENT(OverViewBox, "GD_KeyClassName").text
                    jobDetails["employer"] = KeyProp
                except:
                    jobDetails["employer"] = "Not disclosed"
                    pass
                #
                #
                #
                try:
                    Salary = utils.FINDELEMENT(OverViewBox, "GD_SalaryClassName").text
                    jobDetails["salary"] = Salary
                except:
                    jobDetails["salary"] = "Not disclosed"
                    pass
                #
                #
                try:
                    Location = utils.FINDELEMENT(
                        OverViewBox, "GD_LocationClassName"
                    ).text
                    jobDetails["location"] = Location
                except:
                    jobDetails["location"] = "Not disclosed"
                    pass
                #
                #
                try:
                    DescriptionHTML = utils.FINDELEMENT(
                        DescriptionBox, "GD_JobDescriptionContentClass"
                    ).get_attribute("innerHTML")
                    jobDetails["job_discription_html"] = DescriptionHTML
                except:
                    jobDetails["job_discription_html"] = "Not disclosed"
                    pass
                #
                #
                try:
                    jobDetails["experience"] = "NA"
                except:
                    pass
                #
                jobDetails["tags"] = "NA"
                #
                if callbackFn:
                    callbackFn(jobDetails)
                jobDetailsList.append(jobDetails)
            except:
                pass
            if count > 5:
                break
    return jobDetailsList


if __name__ == "__main__":
    ray.init()
    ray.get(
        [
            start_scraping_glassdoor.remote(
                "Pune", "Data Scientist", callbackFn=ut.print_result
            )
        ]
    )
