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

from .base_tests import BaseTest


class TestAuth(BaseTest):
    """This class collects all the test cases for the users"""

    def test_user_signup(self):
        """Test that a user can signup using a POST request"""
        reg = self.post_user(role="Admin", path="/api/v1/users/32361391")
        self.assertEqual(reg.json['message'], 'Successfully added')
        self.assertEqual(reg.status_code, 201)

    def test_user_login(self):
        """Test that a user can login using a POST request"""
        login = self.admin_login()
        self.assertEqual(login.json['message'], "Success")
        self.assertEqual(login.status_code, 200)

    def test_user_logout(self):
        """Test that the user can logout using a POST request"""
        login = self.admin_login()
        token = login.json['AuthToken']
        logout = self.post(path="/api/v1/auth/signout", data=self.user_admin, auth=token)
        self.assertEqual(logout.status_code, 200)

    def test_invalid_data(self):
        """Test that an unregistered user cannot log in"""
        # generate random username and password
        un_user = {
            "password": "".join(choice(
                                string.ascii_letters) for x in range(randint(7, 10))),
            "id_number": "".join(choice(
                string.ascii_letters) for x in range(randint(7, 10))),
        }
        # attempt to log in
        login = self.post(path="/api/v1/auth/signin", data=un_user, auth=None)
        self.assertEqual(login.status_code, 400)

    def test_an_unregistered_user(self):
        """Test that an unregistered user cannot log in"""
        data = {
            "id_number": 32781319,
            "password": "badadmnsn"
        }
        path = '/api/v1/auth/signin'
        login = self.post(path="/api/v1/auth/signin", data=data, auth=None)
        self.assertEqual(login.status_code, 401)
        self.assertEqual(login.json['message'], "Your details were not found, please sign up")

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy_db()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
