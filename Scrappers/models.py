from dataclasses import dataclass, field
from enum import Enum
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
    SKILLS: list = field(default_factory=list)

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
            "skills": self.SKILLS
        }


@dataclass
class ScrapperResponce:
    ERR: str = None
    DATA: list = field(default_factory=list)
    HAS_ERROR: bool = False

    def __str__(self):
        d = self.dict()
        return str(d)

    def __repr__(self):
        return self.__str__()

    def dict(self):
        return {
            "err": self.ERR,
            "data": self.DATA,
            "has_error": self.HAS_ERROR,
        }


@dataclass
class ErrMsg:
    LOC: str = "NA"
    TITLE: str = "NA"
    ERR: str = None
    DESK: str = "NA"

    def __str__(self):
        d = self.dict()
        return str(d)

    def __repr__(self):
        return self.__str__()

    def __init__(self, location, title, err, desk):
        self.LOC = location
        self.TITLE = title
        self.ERR = err
        self.DESK = desk

    def dict(self):
        return {
            "location": self.LOC,
            "title": self.TITLE,
            "err": self.ERR,
            "desk": self.DESK
        }


def getTotalResponce(responceList):
    data = [item for sublist in responceList for item in sublist.DATA]
    has_error = any([data.HAS_ERROR for data in responceList])
    # get or of all has_error
    err = None
    if has_error:
        err = [data.ERR for data in responceList if data.HAS_ERROR]
    return {'data': data, 'has_error': has_error, 'err': err}


class JOBDESK(Enum):
    GLASSDOOR: str = "glassdoor"
    NAUKRI: str = "naukri"
    INDEED: str = "indeed"


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Job):
            return o.dict()
        if isinstance(o, ErrMsg):
            return o.dict()
        if isinstance(o, ScrapperResponce):
            return o.dict()
        return JSONEncoder.default(self, o)


class CustomJsonEncoder(JsonEncoder):
    def default(self, o):
        if isinstance(o, Job):
            return o.dict()
        if isinstance(o, ErrMsg):
            return o.dict()
        if isinstance(o, ScrapperResponce):
            return o.dict()
        return JsonEncoder.default(self, o)
