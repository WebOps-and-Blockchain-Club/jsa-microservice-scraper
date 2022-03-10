if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

import ray
from typing import Callable
from selenium import webdriver
import Scrappers.utils as ut
from Scrappers.models import Job, JOBDESK as JD, ScrapperResponce as SR, ErrMsg


@ray.remote
def start_scraping_naukri(
    job_location,
    job_title,
    callbackFn: Callable[[dict], None] = None,
    utils: ut = ut,
):
    """
    Scrapes naukri.com for job listings.
    @params:
        job_location: string
        job_title: string
        callbackFn: (Job) => None | None --optional
        utils: Module("utils") -- optional
    Returns:
        list[Job]: list of job listing from glassdoor.com
    """
    # Initialize webdriver
    try:
        jobDetailsList: list[Job] = []
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
        try:
            jobCardListContainer = utils.FINDELEMENT(
                driver, "NK_jobCardListContainer")
            dataset_list = utils.FINDELEMENT(
                jobCardListContainer, "NK_jobCard", True)
            links = []
            for data in dataset_list:
                id = data.get_attribute("data-job-id")
                link = utils.FINDELEMENT(data, "NK_link").get_attribute("href")
                links.append([link, id])
        except:
            utils.tryCloseDreiver(driver)
            raise Exception("cannot get jobs list, NK_jobCardListContainer")

        for link in links:
            driver.get(link[0])
            driver.implicitly_wait(0.3)
            job = Job()

            job.DESK = JD.NAUKRI.value
            job.LINK = link[0]
            job.ID = 'NK_' + str(link[1])
            try:
                detailsBox = utils.FINDELEMENT(driver, "NK_LeftSection")
            except:
                continue

            try:
                job.TITLE = utils.FINDELEMENT(
                    detailsBox, "NK_titleClass"
                ).text
            except:
                pass

            try:
                job.EMPLOYER = utils.FINDELEMENT(
                    detailsBox, "NK_companyName"
                ).text
            except:
                pass

            try:
                job['Experience'] = utils.FINDELEMENT(
                    detailsBox, "NK_Experience"
                ).text
            except:
                pass
            try:
                job.SALARY = utils.FINDELEMENT(
                    detailsBox, "NK_Salary").text
            except:
                pass

            try:
                job.LOCATION = utils.FINDELEMENT(
                    detailsBox, "NK_Location"
                ).text
            except:
                pass

            try:
                job.DESC_HTML = utils.FINDELEMENT(
                    detailsBox, "NK_DescriptionHTML"
                ).get_attribute("innerHTML")
            except:
                pass
            if callbackFn:
                callbackFn(job)
            # data_list.append(jobDetails)
            jobDetailsList.append(job)
        utils.tryCloseDreiver(driver)
        return SR(DATA=jobDetailsList)
    except Exception as e:
        utils.tryCloseDreiver(driver)
        err = ErrMsg(job_location, job_title, str(e), JD.INDEED.value)
        return SR(DATA=jobDetailsList, ERR=err, HAS_ERROR=True)


if __name__ == "__main__":
    ray.init()
    job_list = ray.get(
        [
            start_scraping_naukri.remote(
                "Pune", "Data Scientist", callbackFn=ut.printResult
            )
        ]
    )
    print(job_list)
