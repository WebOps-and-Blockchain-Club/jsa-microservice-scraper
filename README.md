# REST API for Job Posting Scraper

An API to collect the job postings data from [Indeed](https://indeed.com), [Naukri](https://www.naukri.com) and [Glassdoor](https://www.glassdoor.co.in) by selenium package. Currently it's working on [Indeed](https://indeed.com), it will updated soon to get data from [Naukri](https://www.naukri.com) and [Glassdoor](https://www.glassdoor.co.in)

# Setup

1. Clone the repository onto your system
2. Navigate to the root folder of this project
3. To install the neccesary packages `pip install -r requirements.txt`
4. Install the chrome driver on your system
5. Create an `DRIVER_PATH` environment variable with `chrome driver path` value in `.env` file in the project root folder
6. To start the development server, run `python app.py`. Now server will be running on [http://localhost:5000](http://localhost:5000)

# Guide to use API

| URI         | HTTP Method | Inputs                                                                                          | Description                                                                                                             |
| ----------- | ----------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| /           | GET         | null                                                                                            | To ensure server is running                                                                                             |
| /job-search | POST        | JSON form-data with `job` ( Preferred Job Title ) and `location` ( Preferred Location for Job ) | Return the data collected from job posting websites ( Currently it returns data only from [Indeed](https://indeed.com)) |

# Google Colaboratory

1. Master Code to get data from **Indeed**, **Naukri** and **Glassdoor** - [Link](https://colab.research.google.com/drive/1JKp1INK7pCe3QYy34ELcxkvvQVRwjmD6?usp=sharing)
2. Code to get data from **Indeed** - [Link](https://colab.research.google.com/drive/18C01SBBMLyRF-FefuAf2Xb9TVhhjCpF3?usp=sharing)
3. Code to get data from **Naukri** - [Link](https://colab.research.google.com/drive/1-XtGHOZaJ-N8TBYsK9eDvzn8VkU8bD2X?usp=sharing)
4. Code to get data from **Glassdoor** - [Link](https://colab.research.google.com/drive/1vUdJWHE3Lj-I9YY38ZjLLHKoQLfgjyyW?usp=sharing)
