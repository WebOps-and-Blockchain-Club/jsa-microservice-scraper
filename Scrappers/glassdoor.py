if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

from skills_assets.skill_extractor import SkillExtractor
import ray
from typing import Callable
from selenium import webdriver
import Scrappers.utils as ut
from Scrappers.models import Job, JOBDESK as JD, ScrapperResponce as SR, ErrMsg
from skills_assets.skill_extractor import SkillExtractor


@ray.remote
def start_scraping_glassdoor(
    job_location: str,
    job_title: str,
    callbackFn: Callable[[dict], None] = None,
    utils: ut = ut,
):
    """
    Scrapes glassdoor.com for job listings.
    @params:
        job_location: string
        job_title: string
        callbackFn: (Job) => None | None --optional
        utils: Module("utils") -- optional
    Returns:
        list[Job]: list of job listing from glassdoor.com
    """
    try:
        jobDetailsList: list[Job] = []
        # Initialize webdriver
        print("Starting scraping glassdoor")
        driverParams = utils.getDriverParams()
        driver = webdriver.Firefox(**driverParams)
        driver.maximize_window()
        driver.delete_all_cookies()

        # get location id from glassdoor for link
        locationIDLink = f"https://www.glassdoor.co.in/util/ajax/findLocationsByFullText.htm?locationSearchString={job_location}&allowPostalCodes=true"
        driver.get(locationIDLink)
        try:
            jsonRes = utils.FINDELEMENT(driver, "GD_jsonRes").text
            jsonRes = utils.json_to_dict(jsonRes)
            locDet = jsonRes["locations"][0]
            locID = str(locDet["id"])
            locType = locDet["type"]
        except:
            utils.tryCloseDreiver(driver)
            raise Exception("cannot get location id, " + job_location)

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

        # close the login popup if it exists
        def try_close_popup():
            try:
                modalCloseButton = utils.FINDELEMENT(
                    driver, "GD_modalCloseButton")
                modalCloseButton.click()
                driver.implicitly_wait(0.1)
            except:
                pass

        try_close_popup()

        # get all job cards on page
        try:
            dataset = utils.FINDELEMENT(driver, "GD_jobListPath")
            datasetList = utils.FINDELEMENT(
                dataset, "GD_datasetList", is_list=True)
        except:
            utils.tryCloseDreiver(driver)
            raise Exception("cannot get job cards, GD_jobListPath")

        # iterate through job cards
        # for each job card, get the job details
        # and append to jobDetailsList

        for jobCard in datasetList:
            try:
                jobCard.click()
            except:
                driver.implicitly_wait(0.1)
                continue
            try_close_popup()

            # get job details
            job = Job()
            job.DESK = JD.GLASSDOOR.value

            # get job id from glassdoor
            try:
                job.ID = "GD_" + str(jobCard.get_attribute("data-id"))
            except:
                pass

            # get job link
            try:
                anchor = utils.FINDELEMENT(jobCard, "GD_jobLink")
                anchor.get_attribute("href")
                job.LINK = anchor.get_attribute("href")
            except:
                pass
            count = 0

            # after clicking on job card, wait for job details to load
            while count < 20:
                count += 1
                driver.implicitly_wait(0.1)
                try:
                    AllDetailsBox = utils.FINDELEMENT(
                        driver, "GD_DetailsBoxID")
                    OverViewBox = utils.FINDELEMENT(
                        AllDetailsBox, "GD_OverViewBoxClass")
                    Title = utils.FINDELEMENT(
                        OverViewBox, "GD_TitleClassName").text
                    job.TITLE = Title
                    DescriptionBox = utils.FINDELEMENT(
                        driver, "GD_DescriptionBoxId")
                    break
                except:
                    continue
            # if job details are not found, skip job card
            if count >= 10:
                continue

            # get job employer
            try:
                KeyProp = utils.FINDELEMENT(
                    OverViewBox, "GD_KeyClassName").text
                job.EMPLOYER = KeyProp
            except:
                pass

            # get job salary
            try:
                Salary = utils.FINDELEMENT(
                    OverViewBox, "GD_SalaryClassName").text
                job.SALARY = Salary
            except:
                pass

            # get job location
            try:
                Location = utils.FINDELEMENT(
                    OverViewBox, "GD_LocationClassName").text
                job.LOCATION = Location
            except:

                pass

            # get job description HTML
            try:
                Description = utils.FINDELEMENT(
                    DescriptionBox, "GD_JobDescriptionContentClass"
                )
                job.DESC = Description.text
                job.DESC_HTML = Description.get_attribute("innerHTML")
            except:
                pass

            #get job skills
            try:
                skillextractor = SkillExtractor()
                skills = skillextractor.get_skills(job.DESC_HTML)
                job.SKILLS = skills
            except:
                pass

            # call callback function if it exists
            if callbackFn:
                callbackFn(job)

            # add job details to jobDetailsList
            jobDetailsList.append(job)

        # close the browser
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
            start_scraping_glassdoor.remote(
                "Pune", "Data Scientist", callbackFn=ut.printResult
            )
        ]
    )
    # job_list = [item for sublist in job_list for item in sublist]
    print(job_list)
