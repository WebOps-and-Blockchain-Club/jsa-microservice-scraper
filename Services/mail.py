import requests
import json
import ray
import os


@ray.remote
def sendMessage(subject: str, text: str):
    try:
        url = os.environ['BACKEND_URL'] + "/nodemail"
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "text": str(text),
            "subject": str(subject),
            "reciever": os.environ['ADMIN_EMAIL']
        })
        _ = requests.request("POST", url, headers=headers, data=payload)
        print('mail sent')
    except Exception as e:
        print(e)
