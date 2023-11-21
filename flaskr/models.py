import ssl
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError

from flask import url_for

from db import db

class Hospital(db.Document):
    id = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    iri = db.StringField(required=True)
    city = db.StringField(required=True)


class Patient(db.Document):
    id = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    surname = db.StringField(required=True)
    dni = db.StringField(required=True)
    hospital = db.ReferenceField(Hospital)
    doctors = db.ListField(db.ReferenceField("Doctor")) 

class Doctor(db.Document):
    id = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    surname = db.StringField(required=True)
    speciality = db.StringField(required=True)

def sparql(query, endpoint='https://es.dbpedia.org/sparql'):
    FORMATS = ",".join(["application/sparql-results+json",
                    "text/javascript",
                    "application/json"])

    data = {'query': query}

    r = Request(endpoint,
                data=urlencode(data).encode('utf-8'),
                headers={'content-type': 'application/x-www-form-urlencoded',
                         'accept': FORMATS},
                method='POST')


    try:
        try:
            res = urlopen(r)
        except URLError: # If there is a problem with the certificate, try an insecure query
    
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            res = urlopen(r, context=context)
    except HTTPError as e:
        body = e.read().decode()
        raise Exception(f"There is probably something wrong with the query: \n{body}")

    data = res.read().decode('utf-8')
    if res.getcode() == 200:
        try:
            results = json.loads(data)
        except Exception as e:
            raise Exception(f"Could not read JSON: {e}")
    else:
        raise Exception('Error getting results: {}'.format(data))

    print(results)

    info = []

    for result in results["results"]["bindings"]:
        row = {}
        for k, v in result.items():
            row[k] =  v['value']
        info.append(row)
    return info
