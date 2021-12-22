# Import the necessary package
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import request
import os
import time


def scraping():
    # Store the input in JSON
    # Job Title and Location are taken as form input
    Inputs = {}
    Inputs['job'] = request.form.get('job')
    Inputs['location'] = request.form.get('location')

    jobName = Inputs['job']
    location = Inputs['location']

    # Chrome driver setup
    DRIVER_PATH = os.environ['DRIVER_PATH']
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.maximize_window()
    driver.delete_all_cookies()

    # Navigate to https://indeed.com website
    driver.get('https://indeed.com')

    # Input the search parameters - Job Title and Location
    search_job = driver.find_element_by_xpath('//*[@id=\"text-input-what\"]')
    search_job.send_keys([jobName])
    search_location = driver.find_element_by_xpath(
        '//*[@id=\"text-input-where\"]')
    search_location.send_keys([location])

    # Trigger basic search
    time.sleep(1)
    try:
        initial_search_button = driver.find_element_by_xpath(
            '/html/body/div/div[2]/span/div[3]/div[1]/div/div/div/form/div[3]/button')
    except:
        initial_search_button = driver.find_element_by_xpath(
            '/html/body/div/div[2]/span/div[3]/div[1]/div/div/form/button')
    initial_search_button.click()

    # Adding advance search option - Display Limit of 10 and Sort by Date
    advanced_search = driver.find_element_by_xpath(
        "//a[contains(text(),'Advanced Job Search')]")
    advanced_search.click()
    display_limit = driver.find_element_by_xpath(
        '//select[@id="limit"]//option[@value="10"]')
    display_limit.click()
    sort_option = driver.find_element_by_xpath(
        '//select[@id="sort"]//option[@value="date"]')
    sort_option.click()
    search_button = driver.find_element_by_xpath('//*[@id="fj"]')
    search_button.click()

    # Closing irrelevant popup
    time.sleep(1)
    close_popup = driver.find_element_by_xpath('//*[@id=\"popover-x\"]/button')
    close_popup.click()

    # Scraping the data
    # Field that are been scraped - Job Title, Location, Salary, Review, Company
    # Job Cards is been identified based on the class name and the above mentioned fields
    # is taken by looping for all the cards
    data_list = []
    job_card = driver.find_elements_by_xpath(
        '//div[contains(@class,"job_seen_beacon")]')
    for job in job_card:
        # Review Field
        try:
            review = job.find_element_by_xpath(
                './/span[@class="ratingNumber"]').text
        except:
            review = "None"

        # Salary Field
        try:
            salary = job.find_element_by_xpath(
                './/span[@class="salary-snippet"]').text
        except:
            salary = "Not disclosed"

        # Location Field
        try:
            location = job.find_element_by_xpath(
                './/div[contains(@class,"companyLocation")]').text
        except:
            location = Inputs['location']

        # Job Title Field
        try:
            title = job.find_element_by_class_name('jobTitle').text
        except:
            title = Inputs['job']

        # Company Field
        company = job.find_element_by_xpath(
            './/span[@class="companyName"]').text

        # Creating an JSON object of job and adding to the job list
        data = {'title': title, 'company': company,
                'salary': salary, 'location': location, 'review': review}
        data_list.append(data)

    return data_list
