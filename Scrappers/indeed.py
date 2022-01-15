if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

import ray
from typing import Callable
from selenium import webdriver
import Scrappers.utils as ut
from Scrappers.models import Job, JOBDESK as JD


@ray.remote
def start_scraping_indeed(
    job_location,
    job_title,
    callbackFn: Callable[[dict], None] = None,
    utils: ut = ut,
) -> list[Job]:
    print("Starting scraping indeed")
    driverParams = utils.getDriverParams()
    driver = webdriver.Firefox(**driverParams)
    driver.maximize_window()
    driver.delete_all_cookies()
    link = (
        "https://in.indeed.com/"
        + ("-".join([i for i in (job_title.lower()).split()]))
        + "-jobs-in-"
        + ("-".join([i for i in (job_location.lower()).split()]))
    )
    driver.get(link)
    try:
        job_card_list_container = utils.FINDELEMENT(
            driver, "ID_jobListContainer")
        job_card_list = utils.FINDELEMENT(
            job_card_list_container, "ID_jobCard", is_list=True
        )
    except:
        return []
    jobDetailsList: list[Job] = []
    for job_card in job_card_list:
        job = Job()
        job.DESK = JD.INDEED.value
        try:
            job.LINK = job_card.get_attribute("href")
        except:
            pass
        try:
            job.ID = 'IN_' + str(job_card.get_attribute('id'))
        except:
            pass
        try:
            titleBox = utils.FINDELEMENT(job_card, "ID_titleBox")
            job.TITLE = utils.FINDELEMENT(
                titleBox, "ID_title", is_list=True
            )[-1].text
        except:
            pass
        try:
            empAndLoc = utils.FINDELEMENT(job_card, "ID_empAndLoc")
            try:
                job.EMPLOYER = utils.FINDELEMENT(empAndLoc, "ID_emp").text
            except:
                pass
            try:
                job.LOCATION = utils.FINDELEMENT(empAndLoc, "ID_loc").text
            except:
                pass
        except:
            pass
        try:
            job.SALARY = utils.FINDELEMENT(job_card, "ID_salary").text
        except:
            pass
        try:
            job.DESC_HTML = utils.FINDELEMENT(
                job_card, "ID_descHTML"
            ).get_attribute("innerHTML")
        except:
            pass
        if callbackFn:
            callbackFn(job)
        jobDetailsList.append(job)
    driver.close()
    return jobDetailsList


if __name__ == "__main__":
    ray.init()
    job_list = ray.get(
        [
            start_scraping_indeed.remote(
                "Pune", "Data Scientist", callbackFn=ut.printResult
            )
        ]
    )
    job_list = [item for sublist in job_list for item in sublist]
    print(job_list)
