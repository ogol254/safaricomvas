"""
This module collects all the Data Transfer Objects for the API
"""
from flask_restplus import Namespace, fields


class AuthDTO(object):
    """User Data Transfer Object"""
    api = Namespace('auth', description='user authentication and signup resources')
    user = api.model('login request', {
        'username': fields.String(required=True, description="safaricom user's username"),
        'password': fields.String(required=True, description="user's password")
    })
    user_resp = api.model('response to login', {
        'message': fields.String(required=True, description="success or fail message"),
        'AuthToken': fields.String(required=True, description="authentication token"),
        'username': fields.String(required=True, description="safaricom user's username")
    })
    gen_response = api.model('General message response', {
        'message': fields.String(required=True, description="success message"),
    })


class UserDTO(object):
    """docstring for  UserDTO"""
    api = Namespace('auth', description='user and signup resources')
    n_user = api.model('new user request', {
        'username': fields.String(required=True, description="safaricom user's username"),
        'first_name': fields.String(required=True, description="user's first name"),
        'last_name': fields.String(required=True, description="user's last name"),
        'ek_number': fields.String(required=True, description="user's id_number"),
        'email': fields.String(required=True, description="user's email address"),
        'phone_number': fields.String(required=True, description="user's phone number"),
        'password': fields.String(required=True, description="user's password"),
        'position': fields.String(required=False, description="user's address address"),
        'user_level': fields.Integer(required=False, description="permision level")
    })
    n_user_resp = api.model('Response for adding a new user', {
        'message': fields.String(required=True, description="success message"),
        'username': fields.String(required=True, description="safaricom user's username")
    })
    all_users_resp = api.model('Response for getting all users', {
        'message': fields.String(required=True, description="success message"),
        'users': fields.String(required=True, description="User message")
    })

class ProjectDTO(object):
    """ dockstring for the project module """
    api = Namespace('projects', description='project resources')
    n_project = api.model('new project request', {
        'name': fields.String(required=True, description="name of the project"),
        'description': fields.String(required=True, description="description of the project"),
        'start_date': fields.String(required=True, description="start date of the project"),
        'owner': fields.String(required=False, description="the owner of the project"),
        'default_owner': fields.String(required=True, description="depertment owning the project")  
    })
    n_project_resp = api.model('Response for adding a new project', {
        'message': fields.String(required=True, description="success message")
    })

class FileDTO(object):
    """ dockstring for the resources module """
    api = Namespace('files', description='project resources')
    n_file = api.model('new project request', {
        'files': fields.String(required=True, description="url of the file")
    })

class ProjectFileDTO(object):
    """ dockstring for the resources module """
    api = Namespace('files', description='project resources')
    n_file = api.model('new project request', {
        'name': fields.String(required=True, description="name of the file"),
        'description': fields.String(required=False, description="A small description of the project"),
        'link': fields.String(required=True, description="file name store in the database"),
    })
    n_file_resp = api.model('Response for adding a new project', {
        'message': fields.String(required=True, description="success message"),
        'Uplaod data': fields.String(required=True, description="success message")
    })

class AssetsDTO(object):
    """ dockstring for the asset module """
    api = Namespace('assets', description='asset resources')
    n_asset = api.model('new asset request', {
        'type': fields.String(required=True, description="name of the asset"),
        'hostname': fields.String(required=True, description="hostname of  asset"),
        'interface1': fields.String(required=True, description="IP of interface 1 "),
        'interface2': fields.String(required=False, description="IP of interface 2"),
        'interface3': fields.String(required=False, description="IP of interface 3"),
        'peer_system': fields.String(required=False, description="peer system of the asset"),
        'description': fields.String(required=False, description="description of the asset") 
    })
    n_asset_resp = api.model('Response for adding a new asset', {
        'message': fields.String(required=True, description="success message")
    })

    
