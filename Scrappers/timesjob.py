import ray
from typing import Callable
from selenium import webdriver
import Scrappers.utils as ut
from Scrappers.utils import FIELD as F
from Scrappers.utils import JOBDESK as J
from Scrappers.models import Job


@ray.remote
def start_scraping_timesjob(
    job_location,
    job_title,
    callbackFn: Callable[[dict], None] = None,
    utils: ut = ut,
) -> list[Job]:
    def try_close_popup():
        try:
            modal = utils.FINDELEMENT(driver, "TJ_modal")
            modalCloseButton = utils.FINDELEMENT(modal,"TJ_modalclosebtn")
            driver.implicitly_wait(0.1)
            modalCloseButton.click()
        except:
            pass

    print("Starting scraping times job")
    driverParams = utils.getDriverParams()
    driver = webdriver.Firefox(**driverParams)
    driver.maximize_window()
    driver.delete_all_cookies()
    link = ("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={}&txtLocation={}".format(job_title,job_location))
    driver.get(link)

    # get all job cards on page
    try:
        datasetList = utils.FINDELEMENT(driver, "TJ_datalist", True)
    except:
        driver.close()
        return []
    
    try_close_popup()
    jobDetailsList: list[Job] = []
    
    for jobCard in datasetList:

        # check whether job card is present 
        try:
            job_title_heading = utils.FINDELEMENT(jobCard,"h2")
            detailsBox1 = utils.FINDELEMENT(jobCard,"TJ_detailsbox1")
        except:
            continue

        # get job details
        job = Job()
        job.DESK = J.TIMESJOBS

        #get job title and link
        try:
            anchor = utils.FINDELEMENT(job_title_heading,"TJ_titleanchor")
            job.TITLE = anchor.text
            job.LINK = anchor.get_attribute("href")
        except:
            job.TITLE = "NA"
            job.LINK = "NA"

        # get job employer
        try:
            job.EMPLOYER = utils.FINDELEMENT(jobCard, "TJ_companyName").text     
        except:
            job.EMPLOYER = 'NA'

        # get job location
        try:
            job.LOCATION = utils.FINDELEMENT(detailsBox1, "TJ_listitem",is_list= True)[1].text.split("\n")[1]
        except:
            job.LOCATION = job_location

        # add job details to jobDetailsList
        jobDetailsList.append(job)

    # function to scare job desc , salary , job id , job desc html
    def scrape_page2(driver):
        try:
            driver.implicitly_wait(0.1)
            detailsBox1 = utils.FINDELEMENT(driver,"TJ_detailsbox1")
            job_desc = utils.FINDELEMENT(driver,"TJ_JDMAIN").text
            salary = utils.FINDELEMENT(detailsBox1, "TJ_listitem",is_list= True)[1].text.split("\n")[1]
            job_description_html = utils.FINDELEMENT(driver,"TJ_JD").get_attribute('innerHTML')
            job_id = "TJ_" + str(utils.FINDELEMENT(driver,"TJ_jobID").text.split("Job Id: ")[1])
            return job_desc,job_description_html,salary,job_id
        except:
            pass

    for job in jobDetailsList:
        driver.get(job.LINK)
        job.DESC,job.DESC_HTML , job.SALARY , job.ID = scrape_page2(driver)

     # call callback function if it exists
        if callbackFn:
            callbackFn(job)


    # close the browser
    driver.close()
    return jobDetailsList


if __name__ == "__main__":
    ray.init()
    ray.get(
        [
            start_scraping_timesjob.remote(
                "Pune", "Data Scientist", callbackFn=ut.print_result
            )
        ]
    )