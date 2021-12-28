from dataclasses import dataclass
from json import JSONEncoder
from flask.json import JSONEncoder as JsonEncoder


@dataclass
class Job:
    """
    ID: str
    DESK: str
    TITLE: str
    LOCATION: str
    LINK: str
    EMPLOYER: str
    SALARY: str
    DESC: str
    DESC_HTML: str
    """

    ID: str = None
    DESK: str = "NA"
    TITLE: str = "NA"
    LOCATION: str = "NA"
    LINK: str = "NA"
    EMPLOYER: str = "NA"
    SALARY: str = "NA"
    DESC: str = "NA"
    DESC_HTML: str = "NA"

    def __str__(self):
        d = self.dict()
        return str(d)

    def __repr__(self):
        return self.__str__()

    def dict(self):
        return {
            "id": self.ID,
            "desk": self.DESK,
            "title": self.TITLE,
            "location": self.LOCATION,
            "link": self.LINK,
            "employer": self.EMPLOYER,
            "salary": self.SALARY,
            "description": self.DESC,
            "description_html": self.DESC_HTML,
        }


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Job):
            return o.dict()
        return JSONEncoder.default(self, o)


class CustomJsonEncoder(JsonEncoder):
    def default(self, o):
        if isinstance(o, Job):
            return o.dict()
        return JsonEncoder.default(self, o)
