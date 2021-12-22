import ray
import utils
from glassdoor import start_scraping_glassdoor
from naukri import start_scraping_naukri
from indeed import start_scraping_indeed


class Scrapper:
    def __init__(self) -> None:
        ray.init()

    def start_scraping(self, job_location, job_title, callbackFn=None):
        if callbackFn is None:
            callbackFn = utils.print_result
        return ray.get(
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


if __name__ == "__main__":
    scrapper = Scrapper()
    res = scrapper.start_scraping("Hyderabad", "Data Scientist")
    sitesCount = len(res)
    print(f"Total jobs found: {sitesCount}")
    print([len(i) for i in res])
