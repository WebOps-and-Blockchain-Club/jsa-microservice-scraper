import ray
from typing import Callable
from selenium import webdriver
import utils as ut
from utils import FIELD as F
from utils import JOBDESK as J


@ray.remote
def start_scraping_glassdoor(
    job_location,
    job_title,
    callbackFn: Callable[[dict], None] = None,
    utils: ut = ut,
):
    print("Starting scraping glassdoor")
    driverParams = utils.getDriverParams()
    driver = webdriver.Firefox(**driverParams)
    driver.maximize_window()
    driver.delete_all_cookies()

    locationIDLink = f"https://www.glassdoor.co.in/util/ajax/findLocationsByFullText.htm?locationSearchString={job_location}&allowPostalCodes=true"

    driver.get(locationIDLink)

    jsonRes = utils.FINDELEMENT(driver, "GD_jsonRes").text
    jsonRes = ut.json_to_dict(jsonRes)

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
            driver.implicitly_wait(0.1)
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
            driver.implicitly_wait(0.1)
            continue
        try_close_popup()
        jobDetails = {}
        jobDetails[F.JOB_DESK] = J.GLASSDOOR
        count = 0
        try:
            anchor = utils.FINDELEMENT(jobCard, "GD_jobLink")
            anchor.get_attribute("href")
            jobDetails[F.JOB_LINK] = anchor.get_attribute("href")
        except:
            jobDetails[F.JOB_LINK] = F.NA
        while True:
            count += 1
            driver.implicitly_wait(0.1)
            try:
                AllDetailsBox = utils.FINDELEMENT(driver, "GD_DetailsBoxID")
                OverViewBox = utils.FINDELEMENT(AllDetailsBox, "GD_OverViewBoxClass")
                Title = utils.FINDELEMENT(OverViewBox, "GD_TitleClassName").text
                jobDetails[F.JOB_TITLE] = Title
                DescriptionBox = utils.FINDELEMENT(driver, "GD_DescriptionBoxId")
                count = 10
                #
                #
                try:
                    KeyProp = utils.FINDELEMENT(OverViewBox, "GD_KeyClassName").text
                    jobDetails[F.JOB_EMPLOYER] = KeyProp
                except:
                    jobDetails[F.JOB_EMPLOYER] = F.NA
                    pass
                #
                #
                try:
                    Salary = utils.FINDELEMENT(OverViewBox, "GD_SalaryClassName").text
                    jobDetails[F.JOB_SALARY] = Salary
                except:
                    jobDetails[F.JOB_SALARY] = F.NA
                    pass
                #
                #
                try:
                    Location = utils.FINDELEMENT(
                        OverViewBox, "GD_LocationClassName"
                    ).text
                    jobDetails[F.JOB_LOCATION] = Location
                except:
                    jobDetails[F.JOB_LOCATION] = F.NA
                    pass
                #
                #
                try:
                    DescriptionHTML = utils.FINDELEMENT(
                        DescriptionBox, "GD_JobDescriptionContentClass"
                    ).get_attribute("innerHTML")
                    jobDetails[F.JOB_DESCRIPTION_HTML] = DescriptionHTML
                except:
                    jobDetails[F.JOB_DESCRIPTION_HTML] = F.NA
                    pass
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
