import hashlib
import json
import os
import sys
import requests
from requests.auth import HTTPBasicAuth

def get_hash(text):
    return hashlib.sha224(text).hexdigest()

def load_credentials():
    here = os.path.dirname(os.path.realpath(__file__))
    creds = "%s/credentials.json" % here
    if os.path.isfile(creds):
        with open(creds) as fp:
            d = json.load(fp)
            return d["credentials"]
    else:
        return None

def get_file(text):
    credentials = load_credentials()
    here = os.path.dirname(os.path.realpath(__file__))
    text_hash = get_hash(text)
    target = "%s/cache/%s.wav" % (here, text_hash)

    if os.path.isfile(target):
        return target

    r = requests.post("%s/v1/synthesize" % credentials["url"],
        auth=HTTPBasicAuth(credentials["username"], credentials["password"]),
        headers={ "Accept": "audio/wav" },
        json={ "text": text })

    with open(target, "wb") as fp:
        fp.write(r.content)
        return target
