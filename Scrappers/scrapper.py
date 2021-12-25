import ray
import Scrappers.utils as utils
from Scrappers.utils import FIELD as F
from Scrappers.glassdoor import start_scraping_glassdoor
from Scrappers.naukri import start_scraping_naukri
from Scrappers.indeed import start_scraping_indeed


class Scrapper:
    def __init__(self) -> None:
        ray.init()

    def start_scraping(self, job_location, job_title, callbackFn=None) -> list[dict]:
        # if callbackFn is None:
        #     callbackFn = utils.print_result
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
        job_list = [item for sublist in job_list for item in sublist]
        return job_list


if __name__ == "__main__":
    scrapper = Scrapper()
    res = scrapper.start_scraping("Hyderabad", "Data Scientist")
    sitesCount = len(res)
    print(f"Total jobs found: {sitesCount}")
    print([len(i) for i in res])
