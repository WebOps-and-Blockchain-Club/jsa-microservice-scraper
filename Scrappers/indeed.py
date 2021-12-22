import ray
from typing import Callable
from selenium.webdriver.common.by import By
from selenium import webdriver
import utils as ut


@ray.remote
def start_scraping_indeed(
    job_location,
    job_title,
    callbackFn: Callable[[dict], None] = None,
    utils=ut,
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
    data_list = []
    job_card = driver.find_elements(
        By.XPATH, '//div[contains(@class,"job_seen_beacon")]'
    )
    for job in job_card:
        try:
            review = job.find_element(By.XPATH, './/span[@class="ratingNumber"]').text
        except:
            review = "None"
        try:
            salary = job.find_element(By.XPATH, './/div[@class="salary-snippet"]').text
        except:
            salary = "Not disclosed"
        try:
            location = job.find_element(
                By.XPATH, './/div[contains(@class,"companyLocation")]'
            ).text
        except:
            location = job.find_element(
                By.XPATH, './/div[@class,"companyLocation"]'
            ).text
        company = job.find_element(By.XPATH, './/span[@class="companyName"]').text
        try:
            title = job.find_element(By.CLASS_NAME, "jobTitle").text
        except:
            title = job.find_element(
                By.XPATH, './/h2[@class="jobTitle"]'
            ).get_attribute(name="span")
        title_button = job.find_element(By.CLASS_NAME, "jobTitle")
        title_button.click()
        try:
            description = job.find_element(
                By.XPATH, './/div[@class="job-snippet"]'
            ).text
        except:
            description = ""
        url = driver.current_url
        data = {
            "title": title,
            "employer": company,
            "salary": salary,
            "location": location,
            "description": description,
            "url": url,
            "review": review,
            "from": "indeed",
        }
        data_list.append(data)
        callbackFn(data)
    return data_list
