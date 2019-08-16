"""
This module tests the authentication endpoint
Authored by: ogol
"""
import unittest
import json
import string
from contextlib import closing
from random import choice, randint

# local imports
from .. import create_app
from ..db_config import destroy_db, init_db


class BaseTest(unittest.TestCase):
    """docstring for BaseTest"""
    api_prefix = "/api/v1/"

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.user_admin = {
            "id_number": 33133243,
            "first_name": "Abraham",
            "last_name": "Ogol",
            "address": "Nairobi",
            "tell": "0790463533",
            "role": "Admin",
            "password": "ogolpass"
        }

        self.user_clinician = {
            "id_number": 33168643,
            "first_name": "Abraham",
            "last_name": "Ogol",
            "address": "Nairobi",
            "tell": "0790463533",
            "role": "clinician",
            "password": "ogolpass"
        }

        self.user_normal = {
            "id_number": 309382243,
            "first_name": "Abraham",
            "last_name": "Ogol",
            "address": "Nairobi",
            "tell": "0790463533",
            "role": "Normal",
            "password": "ogolpass"
        }

        self.incident = {
            "name": "Marion Okla",
            "location": "Huruma",
            "type": "Third party report",
            "tell": "0790463533",
            "description": "I know of a child being stigmatized about the pregnacy she is having"
        }

        self.facility = {
            "name": "Kenyatta Refferal hospital",
            "location": "Nairobo",
            "contact": "0790463533", 
            "level" : "level 1"
        }

        self.error_msg = "The path accessed / resource requested cannot be found, please check"

        with self.app.app_context():
            self.db = init_db()

    def endpoint_path(self, path):
        return "/api/v1" + path

    def post(self, path, data, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        dto = json.dumps(data)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.post(path=path, data=dto, headers=headers, content_type='application/json')
        return res

    def get(self, path, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.get(path=path, headers=headers, content_type='application/json')
        return res

    def put(self, path, data, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        dto = json.dumps(data)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.put(path=path, data=dto, headers=headers, content_type='application/json')
        return res

    def delete(self, path, auth):
        """ Make API calls for the POST method"""
        paths = self.endpoint_path(path=path)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.delete(path=path, headers=headers, content_type='application/json')
        return res

    def post_user(self, role="", path=""):
        if not path:
            path = "/api/v1/users"
        if role == "Admin":
            res = self.post(path=path, data=self.user_admin, auth=None)
            return res
        elif role == "Normal":
            res = self.post(path=path, data=self.user_normal, auth=None)
            return res
        if role == "clinician":
            res = self.post(path=path, data=self.user_clinician, auth=None)
            return res

    def post_incident(self):
        res = self.post(path="/api/v1/incidents", data=self.incident, auth=None)
        return res

    def post_facilities(self):
        login = self.admin_login()
        token = login.json['AuthToken']
        res = self.post(path="/api/v1/facilities", data=self.facility, auth=token)
        return res

    def post_records(self):
        record = {
            "incident_id": self.post_incident().json['incident_id'],
            "id_num": self.user_admin['id_number'],
            "type": "Third party record",
            "description": "3 months pregnant",
            "location": "Huruma",
            "p_age" : 123,
            "facility_id": self.post_facilities().json['facility_id']
        }
        token = self.admin_login().json['AuthToken']
        res = self.post(path="/api/v1/records", data=record, auth=token)
        return res

    def post_comment(self):
        record = self.post_records()
        token = self.admin_login().json['AuthToken']
        path = "/api/v1/records/{}/comment".format(record.json['record_id'])
        data = {"comment": "Should come back next on monday"}
        res = self.post(path=path, data=data, auth=token)
        return res

    def admin_login(self):
        register = self.post_user(role="Admin", path="/api/v1/users/32361391")
        login = self.post(path="/api/v1/auth/signin", data=self.user_admin, auth=None)
        return login

    def normal_login(self):
        register = self.post_user(role="Normal", path="/api/v1/users/32361391")
        login = self.post(path="/api/v1/auth/signin", data=self.user_normal, auth=None)
        return login

    def clinician_login(self):
        register = self.post_user(role="clinician", path="/api/v1/users/32361391")
        login = self.post(path="/api/v1/auth/signin", data=self.user_clinician, auth=None)
        return login

    def get_headers(self, authtoken=None):
        headers = {
            "Authorization": "Bearer {}".format(authtoken),
            "content_type": 'application/json'
        }
        return headers
