import ray
from typing import Callable
from selenium import webdriver
import Scrappers.utils as ut
from Scrappers.utils import FIELD as F
from Scrappers.utils import JOBDESK as J


@ray.remote
def start_scraping_indeed(
    job_location,
    job_title,
    callbackFn: Callable[[dict], None] = None,
    utils: ut = ut,
):
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
        job_card_list_container = utils.FINDELEMENT(driver, "ID_jobListContainer")
        job_card_list = utils.FINDELEMENT(
            job_card_list_container, "ID_jobCard", is_list=True
        )
    except:
        return []
    job_list = []
    for job_card in job_card_list:
        # job_card.click()
        jobDetails = {}
        jobDetails[F.JOB_DESK] = J.INDEED
        try:
            jobDetails[F.JOB_LINK] = job_card.get_attribute("href")
        except:
            jobDetails[F.JOB_LINK] = F.NA
        try:
            titleBox = utils.FINDELEMENT(job_card, "ID_titleBox")
            jobDetails[F.JOB_TITLE] = utils.FINDELEMENT(
                titleBox, "ID_title", is_list=True
            )[-1].text
        except:
            jobDetails[F.JOB_TITLE] = F.NA
        try:
            empAndLoc = utils.FINDELEMENT(job_card, "ID_empAndLoc")
            try:
                jobDetails[F.JOB_EMPLOYER] = utils.FINDELEMENT(empAndLoc, "ID_emp").text
            except:
                jobDetails[F.JOB_EMPLOYER] = F.NA
            try:
                jobDetails[F.JOB_LOCATION] = utils.FINDELEMENT(empAndLoc, "ID_loc").text
            except:
                jobDetails[F.JOB_LOCATION] = F.NA
        except:
            jobDetails[F.JOB_EMPLOYER] = F.NA
            jobDetails[F.JOB_LOCATION] = F.NA
        try:
            jobDetails[F.JOB_SALARY] = utils.FINDELEMENT(job_card, "ID_salary").text
        except:
            jobDetails[F.JOB_SALARY] = F.NA
        try:
            jobDetails[F.JOB_DESCRIPTION_HTML] = utils.FINDELEMENT(
                job_card, "ID_descHTML"
            ).get_attribute("innerHTML")
        except:
            jobDetails[F.JOB_DESCRIPTION_HTML] = F.NA
        if callbackFn:
            callbackFn(jobDetails)
        job_list.append(jobDetails)
    driver.close()
    return job_list


if __name__ == "__main__":
    ray.init()
    ray.get(
        [
            start_scraping_indeed.remote(
                "Pune", "Data Scientist", callbackFn=ut.print_result
            )
        ]
    )
