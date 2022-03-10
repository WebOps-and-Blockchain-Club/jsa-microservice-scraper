if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

import json
import ray
from Scrappers.models import CustomJSONEncoder, getTotalResponce
import Scrappers.utils as utils
from Scrappers.glassdoor import start_scraping_glassdoor
from Scrappers.naukri import start_scraping_naukri
from Scrappers.indeed import start_scraping_indeed
from Services import mail
import os


class Scrapper:
    def __init__(self):
        pass

    def start_scraping(self, job_location, job_title, callbackFn=None):
        # if callbackFn is None:
        #     callbackFn = utils.printResult
        job_list = ray.get(
            [
                start_scraping_glassdoor.remote(
                    job_location, job_title, callbackFn, utils
                ),
                start_scraping_naukri.remote(
                    job_location, job_title, callbackFn, utils
                ),
                start_scraping_indeed.remote(
                    job_location, job_title, callbackFn, utils
                ),
            ]
        )
        # flaten the list
        responce = getTotalResponce(job_list)
        try:
            if responce['has_error']:
                raise Exception(json.dumps(
                    responce['err'], cls=CustomJSONEncoder))
        except Exception as e:
            mail.sendMessage.remote('Scrapping error', str(e))
        return responce


def main():
    ray.init()
    scrapper = Scrapper()
    res = scrapper.start_scraping("new york", "Data Scientist")
    print(res)


if __name__ == "__main__":
    main()
