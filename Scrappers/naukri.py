import ray
from typing import Callable
from selenium import webdriver
import utils as ut
from utils import FIELD as F
from utils import JOBDESK as J


@ray.remote
def start_scraping_naukri(
    job_location,
    job_title,
    callbackFn: Callable[[dict], None] = None,
    utils: ut = ut,
):
    print("Starting scraping naukri")
    print(ut)
    driverParams = utils.getDriverParams()
    driver = webdriver.Firefox(**driverParams)
    driver.maximize_window()
    driver.delete_all_cookies()
    link = (
        "https://www.naukri.com/"
        + ("-".join([i for i in (job_title.lower()).split()]))
        + "-jobs-in-"
        + ("-".join([i for i in (job_location.lower()).split()]))
    )
    driver.get(link)

    jobCardListContainer = utils.FINDELEMENT(driver, "NK_jobCardListContainer")
    dataset_list = utils.FINDELEMENT(jobCardListContainer, "NK_jobCard", True)
    links = []
    for data in dataset_list:
        link = utils.FINDELEMENT(data, "NK_link").get_attribute("href")
        links.append(link)

    data_list = []
    for link in links:
        driver.get(link)
        driver.implicitly_wait(0.3)
        jobDetails = {}
        try:
            detailsBox = utils.FINDELEMENT(driver, "NK_LeftSection")
        except:
            continue

        jobDetails[F.JOB_LINK] = link
        jobDetails[F.JOB_DESK] = J.NAUKRI

        try:
            jobDetails[F.JOB_TITLE] = utils.FINDELEMENT(
                detailsBox, "NK_titleClass"
            ).text
        except:
            jobDetails[F.JOB_TITLE] = "NA"

        try:
            jobDetails[F.JOB_EMPLOYER] = utils.FINDELEMENT(
                detailsBox, "NK_companyName"
            ).text
        except:
            jobDetails[F.JOB_EMPLOYER] = "NA"

        try:
            jobDetails["experience"] = utils.FINDELEMENT(
                detailsBox, "NK_Experience"
            ).text
        except:
            jobDetails["experience"] = "NA"

        try:
            jobDetails[F.JOB_SALARY] = utils.FINDELEMENT(detailsBox, "NK_Salary").text
        except:
            jobDetails[F.JOB_SALARY] = "NA"

        try:
            jobDetails[F.JOB_LOCATION] = utils.FINDELEMENT(
                detailsBox, "NK_Location"
            ).text
        except:
            jobDetails[F.JOB_LOCATION] = "NA"

        try:
            jobDetails[F.JOB_DESCRIPTION_HTML] = utils.FINDELEMENT(
                detailsBox, "NK_DescriptionHTML"
            ).get_attribute("innerHTML")
        except:
            jobDetails[F.JOB_DESCRIPTION_HTML] = "NA"
        if callbackFn:
            callbackFn(jobDetails)
        data_list.append(jobDetails)
    print(data_list)
    return data_list


if __name__ == "__main__":
    ray.init()
    ray.get(
        [
            start_scraping_naukri.remote(
                "Pune", "Data Scientist", callbackFn=ut.print_result
            )
        ]
    )
