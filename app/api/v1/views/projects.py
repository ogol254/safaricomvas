import os
import re
import json
import string
import werkzeug
from random import randint
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

from flask_restplus import Resource, reqparse
from flask import jsonify, make_response, request, g, jsonify, redirect, url_for

from ..utils.email import Email
from ..utils.serializers import ProjectDTO
from ..models.auth_models import AuthModel 
from ..models.projects_model import ProjectModel 
from ..utils.auth_validation import auth_required, _validate_project


api = ProjectDTO().api
new_project = ProjectDTO().n_project
new_project_resp = ProjectDTO().n_project_resp


def get_project_id(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    num_id = randint(range_start, range_end)
    if ProjectModel().check_exists(table="projects", field="_id", data=num_id) == False:return num_id
    else: get_project_id(4)

########################################################################## POST AND GET PROJECTS #########################################################################################

@api.route("/")
class Projects(Resource):
    """This class collects the methods for the auth/signin method"""
    @api.marshal_with(new_project_resp, code=201)
    @api.expect(new_project, validate=True)
    @auth_required
    def post(self):
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)
        try:
            name = body['name']
            description = body['description'].strip()
            start_date = body['start_date'].strip()
            owner = body['owner'].strip()
            default_owner = body['default_owner'].strip()
            
        except (KeyError, IndexError) as e:
            raise BadRequest

        project_data = {
            "_id": get_project_id(4),
            "name": name,
            "description": description,
            "start_date": start_date,
            "owner": owner,
            "default_owner": default_owner,
            "created_by": g.user
        }
        _validate_project(project_data)
        p = ProjectModel(**project_data)
        if p.check_exists(table="users", field="username", data=owner) == False:
            raise BadRequest("There is no user with such a username")
        else:
            resp = p.save()
            token = p.encode_auth_token(g.user).decode("utf-8")
            admins = p.get_admins()
            for admin in admins:
                e=Email([admin['email']])
                e.project_a_admin(admin['username'], g.user, name, request.host_url+'api/v1/projects/'+str(project_data['_id'])+'/approve?token='+str(token))
        
            en = Email([ProjectModel().get_user_username(g.user)[5]])
            en.p_self_notifier(g.user, name)

            respn = {
                "message": "Successfully created",
            }

        return respn, 201

    @auth_required
    def get(self):
        

        resp = ProjectModel().get_projects()
        users_list = {
            "quantity" : len(resp),
            "Projects": resp
        }
        return resp, 200

########################################################################## DEL, UPDATE, GET SINGLE #########################################################################################

@api.route("/<int:project_id>")
class ProjectSpecific(Resource):
    """docstring for ClassName"""
    @auth_required
    def get(self, project_id):
        if ProjectModel().check_exists("projects", "_id", project_id) == False:
            raise NotFound("No such project in our record")
        resp = ProjectModel().get_specific_project(project_id)
        users = {"Project": resp}
        return resp, 200

    

    @auth_required
    def put(self, project_id):
        if ProjectModel().check_exists("projects", "_id", project_id) == False:
            raise NotFound("No such project in our record")

        who = ProjectModel().get_specific_project(project_id)[0]['created_by']
        if who == g.user or ProjectModel().get_user_username(g.user)[4] == 0:
            req_data = request.data.decode().replace("'", '"')
            if not req_data:
                raise BadRequest("Provide data in the request")
            body = json.loads(req_data)
            _validate_project(body)
            for field, value in body.items():
                ProjectModel().update_item(table="projects",field=field,data=value,item_field="_id",item_id=project_id)
            resp = {"message": "Successfully Updated" }
            return resp, 200
        else:
            raise Unauthorized("You are not permitted to preform this operation")

########################################################################## PROJECT APPROVAL #########################################################################################

@api.route("/<int:project_id>/approve")
class ProjectApprova(Resource):
    """docstring for ClassName"""
    
    @auth_required
    def post(self, project_id):
        # Project approval
        if ProjectModel().check_exists("projects", "_id", project_id) == False:
            raise NotFound("No such project in our record")
        
        if ProjectModel().get_user_username(g.user)[4] == 0:
            if not request.args.get('token'):
                raise BadRequest("Bad url, Kindly confirm that it has a token and try again")
            else:
                token = request.args.get('token')
                if ProjectModel().decode_auth_token(token) == ProjectModel().get_specific_project(project_id)[0]['created_by']:
                    ProjectModel().update_item(table="projects",field="status",data=1,item_field="_id",item_id=project_id)
                    AuthModel().logout_user(token) #Destroy token
                    resp = {"message": "Approved successfully"}
                    return resp, 200
                else:
                    raise BadRequest("The token provided is invalid and we could not validate it")
        else:
            raise Unauthorized("You are not permitted to preform this operation")

########################################################################## GET PROJECTS PER USERNAME #########################################################################################

@api.route("/user")
class GetProjectWithUsername(Resource):

    @auth_required
    def get(self):
        
        offset = request.args.get('offset') 
        limit = request.args['limit'] 

        if not limit:
            limit = 10
        if not offset:
            offset = 0
       
        resp = ProjectModel().get_projects_user(g.user, limit, offset)
        users_list = {
                "quantity" : len(resp),
                "Projects": resp
            }
        return users_list, 200
        