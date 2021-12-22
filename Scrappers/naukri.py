import ray
from typing import Callable
from selenium import webdriver
import utils as ut


@ray.remote
def start_scraping_naukri(
    job_location,
    job_title,
    callbackFn: Callable[[dict], None] = None,
    utils=ut,
):
    print("Starting scraping naukri")
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

        jobDetails["job_url"] = link
        jobDetails["from"] = "naukri"

        try:
            jobDetails["title"] = utils.FINDELEMENT(detailsBox, "NK_titleClass").text
        except:
            jobDetails["title"] = "NA"

        try:
            jobDetails["employer"] = utils.FINDELEMENT(
                detailsBox, "NK_companyName"
            ).text
        except:
            jobDetails["employer"] = "NA"

        try:
            jobDetails["experience"] = utils.FINDELEMENT(
                detailsBox, "NK_Experience"
            ).text
        except:
            jobDetails["experience"] = "NA"

        try:
            jobDetails["salary"] = utils.FINDELEMENT(detailsBox, "NK_Salary").text
        except:
            jobDetails["salary"] = "NA"

        try:
            jobDetails["location"] = utils.FINDELEMENT(detailsBox, "NK_Location").text
        except:
            jobDetails["location"] = "NA"

        try:
            jobDetails["job_discription_html"] = utils.FINDELEMENT(
                detailsBox, "NK_DescriptionHTML"
            ).get_attribute("innerHTML")
        except:
            jobDetails["job_discription_html"] = "NA"
        if callbackFn:
            callbackFn(jobDetails)
        data_list.append(jobDetails)
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
