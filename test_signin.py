import requests
import random
import base64
from pyjiit.encryption import deserialize_payload, serialize_payload, generate_local_name
import os


USERNAME = os.getenv("UID")
PASSWORD = os.getenv("PASS")

if USERNAME is None or PASSWORD is None:
    print("export USERNAME and PASSWORD to env.")
    exit(1)

payload = {
    "username": USERNAME,
	"usertype":"S",
    "captcha": {
        "captcha": "cfmab",
        "hidden": "gMWqdbxEjE8="
    }
}
enc_payload = serialize_payload(payload)

URL = "https://webportal.jiit.ac.in:6011/StudentPortalAPI/token/pretoken-check"
headers = {
    "LocalName": generate_local_name()
}

resp = requests.post(URL, data=enc_payload, headers=headers).json()

if resp["status"]['responseStatus'] != 'Success':
    print("Error signing in!")
    exit(1)

URL = "https://webportal.jiit.ac.in:6011/StudentPortalAPI/token/generate-token1"
payload: dict = resp['response']
payload.pop('rejectedData')

payload['Modulename'] = 'STUDENTMODULE'
payload['passwordotpvalue'] = PASSWORD
enc_payload = serialize_payload(payload)

headers = {
    "LocalName": generate_local_name()
}
resp = requests.post(URL, data=enc_payload, headers=headers)

from pprint import pprint

pprint(resp.json())
