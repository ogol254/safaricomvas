# """
# This module tests the authentication endpoint
# Authored by: ogol
# """
# import unittest
# import json
# import string
# from contextlib import closing
# from random import choice, randint

# # local imports
# from .. import create_app
# from ..db_config import destroy_db, init_db

# from .base_tests import BaseTest


# class TestUser(BaseTest):
#     """This class collects all the test cases for the users"""

#     def test_resgistering_a_user_admin(self):
#         """Test that an admin user can register a new user using a POST request"""
#         login = self.admin_login()
#         token = login.json['AuthToken']
#         add_user = self.post(path="/api/v1/users", data=self.user_normal, auth=token)
#         self.assertEqual(add_user.json['message'], 'Successfully added')
#         self.assertEqual(add_user.status_code, 201)

#     def test_resgistering_a_user_normal(self):
#         """Test that a normal user cannot register a new user using a POST request"""
#         login = self.normal_login()
#         token = login.json['AuthToken']
#         add_user = self.post(path="/api/v1/users", data=self.user_admin, auth=token)
#         self.assertEqual(add_user.json['message'], 'You are not permitted to preform this operation')
#         self.assertEqual(add_user.status_code, 401)

#     def test_getting_all_users_admin(self):
#         """Test that an admin user can get all users using a GET request"""
#         login = self.admin_login()
#         token = login.json['AuthToken']
#         add_user = self.get(path="/api/v1/users", auth=token)
#         self.assertEqual(add_user.status_code, 200)

#     def test_getting_all_users_clinician(self):
#         """Test that an clincian user cannot get all users using a GET request"""
#         login = self.clinician_login()
#         token = login.json['AuthToken']
#         add_user = self.get(path="/api/v1/users", auth=token)
#         self.assertEqual(add_user.status_code, 401)

#     def test_getting_user_records_clinician(self):
#         """Test that a user can get all his/he rrecords using a GET request"""
#         login = self.clinician_login()
#         token = login.json['AuthToken']
#         path = "/api/v1/users/records/{}".format(int(login.json['id_number']))
#         add_user = self.get(path=path, auth=token)
#         self.assertEqual(add_user.status_code, 200)

#     def test_getting_user_icnidents_clinician(self):
#         """Test that an admin/clinician user can get all  incidents using a GET request"""
#         login = self.clinician_login() 
#         token = login.json['AuthToken']
#         path = "/api/v1/users/incidents/{}".format(int(login.json['id_number']))
#         add_user = self.get(path=path, auth=token)
#         self.assertEqual(add_user.status_code, 200)

#     def test_getting_user_icnidents_normal(self):
#         """Test that a normal user cannot get all his/he incidents using a GET request"""
#         login = self.normal_login()
#         token = login.json['AuthToken']
#         path = "/api/v1/users/incidents/{}".format(int(login.json['id_number']))
#         add_user = self.get(path=path, auth=token)
#         self.assertEqual(add_user.status_code, 401)

#     def test_sending_request_without_header(self):
#         """Test sending a bad request"""
#         path = "/api/v1/users/incidents/{}".format(int(login.json['id_number']))
#         add_user = self.get(path=path, auth=None)
#         self.assertEqual(add_user.status_code, 400)

#     def tearDown(self):
#         """This function destroys objests created during the test run"""

#         with self.app.app_context():
#             destroy_db()
#             self.db.close()


# if __name__ == "__main__":
#     unittest.main()
