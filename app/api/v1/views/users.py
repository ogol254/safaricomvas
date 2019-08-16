import os
import re
import json
import string
import werkzeug
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden, Conflict

from flask_restplus import Resource, reqparse
from flask import jsonify, make_response, request, g, jsonify, redirect, url_for

from ..utils.email import Email
from ..utils.serializers import UserDTO
from ..models.user_models import UserModel
from ..utils.auth_validation import auth_required, _validate_user


api = UserDTO().api
new_user = UserDTO().n_user
new_user_resp = UserDTO().n_user_resp
users_resp = UserDTO().all_users_resp

APP_ROOT = "C:\\Users\\aogol\\Desktop\\asset"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route("/")
class Users(Resource):
    """This class collects the methods for the auth/signin method"""
    # @api.marshal_with(new_user_resp, code=201)
    @api.expect(new_user, validate=True)
    @auth_required
    def post(self):
        """This endpoint allows an unregistered user to sign up."""

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)
        try:
            username = body['username']
            first_name = body['first_name'].strip()
            last_name = body['last_name'].strip()
            ek_number = body['ek_number'].strip()
            email = body['email'].strip()
            phone_number = body['phone_number'].strip()
            password = body['password'].strip()
            user_level = body['user_level'] 
            if not user_level:
                user_level = 1
        except (KeyError, IndexError) as e:
            raise BadRequest

        user_data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "ek_number": ek_number,
            "email": email,
            "phone_number": phone_number,
            "password": password,
            "user_level": user_level
        }
        _validate_user(user_data)
        user = UserModel(**user_data)
        if user.check_exists(table="users", field="username", data=username) == True:
            raise Conflict("There is a user with such a username")
        elif user.check_exists(table="users", field="email", data=email) == True:
            raise Conflict("There is a user with such an email")
        elif user.check_exists(table="users", field="ek_number", data=ek_number) == True:
            raise Conflict("There is a user with the same EK number")
        else:
            resp = user.save()
            e = Email([email])
            e.welcome_text(first_name+' '+last_name, password, username)
            respn = {
                "message": "Successfully added",
                "username" : username
            }

        return respn, 201

    @auth_required
    def get(self):
        resp = UserModel().get_users()
        return resp, 200


@api.route("/<string:username>")
class UserSpecific(Resource):
    """docstring for ClassName"""
    @auth_required
    def get(self, username):
        if UserModel().check_exists("users", "username", username) == False:
            raise NotFound("No such user in our record")
        resp = UserModel().get_specific_user(username)
        return resp, 200

    @auth_required
    def put(self, username):
        if UserModel().check_exists("users", "username", username) == False:
            raise NotFound("No such user in our record")
        if username == g.user or UserModel().get_user_username(g.user)[4] == 0:
            req_data = request.data.decode().replace("'", '"')
            if not req_data:
                raise BadRequest("Provide data in the request")
            body = json.loads(req_data)
            _validate_user(body)
            for field, value in body.items():
                if field == "username" or field == "user_level":
                    raise Unauthorized("You are not permitted to preform this operation")
                elif field == "email" :
                    if UserModel().check_exists(table="users", field="email", data=value) == True:
                        raise Conflict("There is a user with such an email")
                    else :
                        UserModel().update_item(table="users",field=field,data=value,item_field="username",item_id=username)  
                elif field == "ek_number":
                    if UserModel().check_exists(table="users", field="ek_number", data=value) == True:
                        raise Conflict("There is a user with the same EK number")
                    else:
                        UserModel().update_item(table="users",field=field,data=value,item_field="username",item_id=username)
                else:
                    UserModel().update_item(table="users",field=field,data=value,item_field="username",item_id=username)
            
            new_user = {"message" : "Successfully Updated"}
            return new_user, 200
        else:
            raise Unauthorized("You are not permitted to preform this operation")
    
    @auth_required
    def post(self, username):
        if UserModel().check_exists("users", "username", username) == False:
            raise NotFound("No such user in our record")
        if username == g.user or UserModel().get_user_username(g.user)[4] == 0:

            target = os.path.join(APP_ROOT, 'files/profile')
            if not os.path.isdir(target):
                os.mkdir(target)
            image = request.files["image"]
            filename = image.filename
            if filename == '':
                raise BadRequest("No file has been selected")
            if image and allowed_file(filename):
                destination = "/".join([target, filename])
                image.save(destination)
                UserModel().update_item(table="users",field="profile", data=filename, item_field="username",item_id=username)
                respn = { "message": "Successfully updated" }
                return respn, 201
            else:
                raise BadRequest("Allowed file types are png, jpg, jpeg ")
		
        else:
            raise Unauthorized("You are not permitted to preform this operation")


    def default(self, o):
        return o.__dict__  
			