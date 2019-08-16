import re
import json
import string
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

from flask_restplus import Resource
from flask import jsonify, make_response, request, g
#local imports
from ..models.auth_models import AuthModel
from ..utils.serializers import AuthDTO
from ..utils.auth_validation import auth_required, _validate_user

api = AuthDTO().api
login_user = AuthDTO().user
_user_resp = AuthDTO().user_resp
gen_response = AuthDTO().gen_response


@api.route("/signin")
class AuthLogin(Resource):
 
    @api.expect(login_user, validate=True)
    def post(self):
        """This endpoint allows an unregistered user to sign up."""
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        login_details = json.loads(req_data)
        username = login_details['username'].strip()
        password = login_details['password'].strip()

        login_data = {
            "username": username,
            "password": password
        }

        _validate_user(login_data)
        user = AuthModel(**login_data)
        record = AuthModel().get_user_username(username)
        if not record:
            return make_response(jsonify({
                "message": "Your details were not found, please sign up"
            }), 401)

        first_name, last_name, passwordharsh, username, user_level, email = record
        if not check_password_hash(passwordharsh, password):
            raise Unauthorized("Username / Password do not match")

        token = user.encode_auth_token(username)
        resp = {
            "message": "Success",
            "AuthToken": "{}".format(token.decode('utf-8')),
            "username": username
        }

        return resp, 200

@api.marshal_with(gen_response, code=200)
@api.route('/signout')
class AuthLogout(Resource):
    """This class collects the methods for the  endpoint"""

    def post(self):
        """This endpoint allows a registered user to logout."""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest("authorization header provided. This resource is secured.")
        auth_token = auth_header.split(" ")[1]
        response = AuthModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # token is either invalid or expired
            raise Unauthorized("Token is invalid")
        else:
            # the token decoded succesfully
            # logout the user
            user_token = AuthModel().logout_user(auth_token)
            resp = dict()
            return {"message": "logout successful"}, 200

@auth_required
@api.route('/validate')
class AuthValidate(Resource):
    """This class collects the methods for the questions endpoint"""
    docu_string = "This endpoint validates a token"

    @api.doc(docu_string)
    @auth_required
    def post(self):
        """This endpoint validates a token"""
        resp = {
            "message": "Valid",
            "username": g.user
        }
        return resp, 200
