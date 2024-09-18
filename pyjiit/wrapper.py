from datetime import datetime
from pprint import pformat
from pyjiit.encryption import serialize_payload, generate_local_name
from pyjiit.registration import Registrations
from pyjiit.token import Captcha
from pyjiit.default import CAPTCHA
from pyjiit.exceptions import APIError, LoginError, NotLoggedIn, SamePasswordError, SessionExpired
from pyjiit.attendance import AttendanceMeta, AttendanceHeader, Semester

import requests
import json
import base64
import datetime


API = "https://webportal.jiit.ac.in:6011/StudentPortalAPI"

def authenticated(method):
    def wrapper(*a, **kw):
        if a[0].session is None:
            raise NotLoggedIn

        if a[0].session.expiry < datetime.datetime.now():
            raise SessionExpired

        return method(*a, **kw)
    return wrapper

class WebportalSession:
    def __init__(self, resp: dict) -> None:
        self.raw_response = resp
        self.regdata: dict = resp['regdata']
        
        institute = self.regdata['institutelist'][0]
        self.institute: str = institute['label']
        self.instituteid: str = institute['value']
        self.memberid: str = self.regdata['memberid']
        
        self.userid: str = self.regdata['userid']

        self.token: str = self.regdata['token']
        expiry_timestamp = json.loads(base64.b64decode(self.token.split(".")[1]))['exp']
        self.expiry = datetime.fromtimestamp(expiry_timestamp)
            
        self.clientid = self.regdata["clientid"]
        self.membertype = self.regdata["membertype"]
        self.name = self.regdata["name"]
    
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "LocalName": generate_local_name()
        }

class Webportal:
    def __init__(self) -> None:
        self.session: WebportalSession | None = None
    
    def __hit(self, *args, **kwargs):
        exception = APIError

        if kwargs.get("exception"):
            exception = kwargs["exception"]
            kwargs.pop("exception")

        if kwargs.get("authenticated"): 
            header = self.session.get_headers() # Assumes calling method is authenticated
            kwargs.pop("authenticated")
        else:
            header = {"LocalName": generate_local_name()}

        if kwargs.get("headers"):
            kwargs["headers"].update(header)
        else:
            kwargs["headers"] = header
        

        resp = requests.request(*args, **kwargs).json()
        if resp["status"]["responseStatus"] != "Success":
            raise exception("status:\n"+pformat(resp["status"]))

        return resp


    def student_login(self, username: str, password: str, captcha: Captcha = CAPTCHA) -> WebportalSession:
        pretoken_endpoint = "/token/pretoken-check"
        token_endpoint = "/token/generate-token1"     


        payload = {
            "username": username,
            "usertype": "S",
            "captcha": captcha.payload()
        }
        payload = serialize_payload(payload)

        resp = self.__hit("POST", API+pretoken_endpoint, data=payload, exception=LoginError)

        payload = resp["response"]
        payload.pop("rejectedData")

        payload['Modulename'] = 'STUDENTMODULE'
        payload['passwordotpvalue'] = password
        payload = serialize_payload(payload)

        resp = self.__hit("POST", API+token_endpoint, data=payload, exception=LoginError)
        
        self.session = WebportalSession(resp['response'])

        return self.session

    def get_captcha(self):
        ENDPOINT = "/token/getcaptcha"

        resp = self.__hit("GET", API+ENDPOINT)

        return resp["response"]
    
    @authenticated
    def get_student_bank_info(self):
        ENDPOINT = "/studentbankdetails/getstudentbankinfo"

        payload = {
                "instituteid": self.session.instituteid,
                "studentid": self.session.memberid
        }
        resp = self.__hit("POST", API+ENDPOINT, json=payload, authenticated=True)

        return resp["response"]

    @authenticated
    def get_attendance_meta(self):
        ENDPOINT = "/StudentClassAttendance/getstudentInforegistrationforattendence"

        payload = {
            "clientid": self.session.clientid,
            "instituteid": self.session.instituteid,
            "membertype": self.session.membertype
        }
        
        resp = self.__hit("POST", API+ENDPOINT, json=payload, authenticated=True)

        return AttendanceMeta(resp["response"])

    @authenticated
    def get_attendance(self, header: AttendanceHeader, semester: Semester):
        ENDPOINT = "/StudentClassAttendance/getstudentattendancedetail"
        
        payload = {
            "clientid": self.session.clientid,
            "instituteid": self.session.instituteid,
            "registrationcode": semester.registration_code,
            "registrationid": semester.registration_id,
            "stynumber": header.stynumber
        }
        
        resp = self.__hit("POST", API+ENDPOINT, json=payload, authenticated=True)
        
        return resp["response"]

    @authenticated
    def set_password(self, old_pswd: str, new_pswd: str):
        ENDPOINT = "/clxuser/changepassword"

        payload = {
            "membertype": self.session.membertype,
            "oldpassword": old_pswd,
            "newpassword": new_pswd,
            "confirmpassword": new_pswd
        }

        resp = self.__hit("POST", API+ENDPOINT, json=payload, authenticated=True, exception=AccountAPIError)

    
    @authenticated
    def get_registered_semesters(self):
        ENDPOINT = "/reqsubfaculty/getregistrationList"

        payload = {
            "instituteid": self.session.instituteid,
            "studentid": self.session.memberid
        }

        resp = self.__hit("POST", API+ENDPOINT, json=payload, authenticated=True)
        
        return [Semester.from_json(i) for i in resp["response"]["registrations"]]

    @authenticated
    def get_registered_subjects_and_faculties(self, semester: Semester):
        ENDPOINT = "/reqsubfaculty/getfaculties"

        payload = {
            "instituteid": self.session.instituteid,
            "studentid": self.session.memberid,
            "registrationid": semester.registration_id
        }

        resp = self.__hit("POST", API+ENDPOINT, json=payload, authenticated=True)

        return Registrations(resp["response"])


