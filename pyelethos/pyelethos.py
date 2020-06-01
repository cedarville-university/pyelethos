# Copyright 2020 Cedarville University
# Based on code from:  https://github.com/ellucianEthos/python-pubsub-demo

import requests
import datetime
from dateutil.parser import *


class Pyelethos:
    ethos_integration_url = "https://integrate.elluciancloud.com"
    api_key = ''
    jwt = ''

    def __init__(self, api_key):
        self.api_key = api_key

    def get_jwt(self):
        if self.api_key:
            headers = {'Authorization': "Bearer " + self.api_key}
            response = requests.request("POST", self.ethos_integration_url + "/auth", headers=headers)

            if response.status_code == 200:
                self.jwt = response.text
            # print(self.jwt)
            elif response.status_code == 406:
                raise Exception('Api Key is invalid', response.status_code, response.text)
            else:
                raise Exception('Error calling pyelethos authorization endpoint', response.status_code,
                                response.text)
        else:
            raise Exception('Api Key not defined')

    def send_change_notification(self, change_notification, retry=True):
        if not self.jwt:
            self.get_jwt()

        headers = {
            'Authorization': "Bearer " + self.jwt,
            'Content-Type': 'application/vnd.hedtech.change-notifications.v2+json'}
        response = requests.request("POST", self.ethos_integration_url + "/publish", headers=headers,
                                    json=change_notification)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401 and retry:
            print('JWT has expired')
            self.get_jwt()
            return self.send_change_notification(change_notification, retry=False)
        else:
            raise Exception('Error calling pyelethos consume endpoint send_change_notification', response.status_code,
                            response.text)

    def get_change_notifications(self, retry=True):
        if not self.jwt:
            self.get_jwt()

        headers = {
            'Authorization': "Bearer " + self.jwt,
            'Accept': 'application/vnd.hedtech.change-notifications.v2+json'}
        response = requests.request("GET", self.ethos_integration_url + "/consume", headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401 and retry:
            print('JWT has expired')
            self.get_jwt()
            return self.get_change_notifications(retry=False)
        else:
            raise Exception('Error calling Ethos Integration consume endpoint', response.status_code, response.text)

    def get_person(self, person_to_get, retry=True):
        if not self.jwt:
            self.get_jwt()

        response = requests.get(
            url=self.ethos_integration_url + "/api/persons",
            params={
                "criteria": "{\"credentials\":[{\"type\":\"colleaguePersonId\",\"value\":\"" + person_to_get + "\"}]}",
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/vnd.hedtech.applications.v2+json",
                "Authorization": "Bearer " + self.jwt,
                "Accept-Charset": "UTF-8",
            },
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401 and retry:
            print('JWT has expired')
            self.get_jwt()
            return self.get_person(person_to_get, retry=False)
        else:
            raise Exception('Error calling pyelethos endpoint get_person', response.status_code, response.text)

    def get_open_terms(self, retry=True):
        if not self.jwt:
            self.get_jwt()

        response = requests.get(
            url=self.ethos_integration_url + "/api/academic-periods",
            params={
                "criteria": "{\"registration\":\"open\"}",
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/vnd.hedtech.applications.v16.1.0+json",
                "Authorization": "Bearer " + self.jwt,
                "Accept-Charset": "UTF-8",
            },
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401 and retry:
            print('JWT has expired')
            self.get_jwt()
            return self.get_open_terms(retry=False)
        else:
            raise Exception('Error calling pyelethos endpoint get_open_terms', response.status_code, response.text)

    def get_term_by_code(self, termid, retry=True):
        if not self.jwt:
            self.get_jwt()

        response = requests.get(
            url=self.ethos_integration_url + "/api/academic-periods",
            params={
                "criteria": "{\"code\":\"" + termid + "\"}",
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/vnd.hedtech.applications.v16.1.0+json",
                "Authorization": "Bearer " + self.jwt,
                "Accept-Charset": "UTF-8",
            },
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401 and retry:
            print('JWT has expired')
            self.get_jwt()
            return self.get_open_terms(retry=False)
        else:
            raise Exception('Error calling pyelethos endpoint get_term_by_code', response.status_code, response.text)

    def get_terms_starting_after(self, passeddate, retry=True):
        if not self.jwt:
            self.get_jwt()

        if isinstance(passeddate, str):
            searchdate = parse(passeddate)
        elif isinstance(passeddate, datetime.date):
            searchdate = passeddate
        elif isinstance(passeddate, datetime.datetime):
            searchdate = passeddate
        else:
            searchdate = "2020-01-01"

        print(searchdate.strftime("%Y-%m-%d"))

        response = requests.get(
            url=self.ethos_integration_url + "/api/academic-periods",
            params={
                "criteria": "{\"startOn\":{\"$gte\":\"" + searchdate.strftime("%Y-%m-%d") + "\"}}",
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/vnd.hedtech.applications.v16.1.0+json",
                "Authorization": "Bearer " + self.jwt,
                "Accept-Charset": "UTF-8",
            },
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401 and retry:
            print('JWT has expired')
            self.get_jwt()
            return self.get_open_terms(retry=False)
        else:
            raise Exception('Error calling pyelethos endpoint get_term_starting_after', response.status_code,
                            response.text)
