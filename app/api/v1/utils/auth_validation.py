
"""
This module collects the utilities for authorization.
"""
from functools import wraps

from flask import request, g
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden, Conflict

from ..models.base_model import BaseModel

import json
import re
import string

def auth_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        """Checks the validity of the header and raises a corresponding error"""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise BadRequest("This endpoint requires authorization")
        auth_token = auth_header.split(" ")[1]
        response = BaseModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            raise Unauthorized("You are not authorized to access this resource")
        else:
            g.user = response
            return func(*args, **kwargs)
    return wrap


def _validate_user(user):
    """This function validates the user input and rejects or accepts it"""
    for key, value in user.items():
        # ensure keys have values
        if not value: raise BadRequest("{} is lacking. It is a required field".format(key))
        if key == "username" or key == "password":
            if len(value) < 5: raise BadRequest("The {} provided is too short".format(key))
            elif len(value) > 15: raise BadRequest("The {} provided is too long".format(key))
        if key == "first_name" or key == "last_name" or key == "username":
            for i in value:
                if i not in string.ascii_letters: raise BadRequest("{} cannot have non-alphabetic characters.".format(key))
        if key == "email":
            if not re.match(r'^[a-zA-Z0-9_.+-]+@(?:(?:[a-zA-Z0-9-]+\.)?[a-zA-Z]+\.)?(safaricom)\.co.ke$', value): raise BadRequest("The email provided is not a safaricom email")
        if key == "password":
            if not re.match(r'^(?=.*[A-Z])(?=.*[!@#$&*\^%\*\.])(?=.*[0-9])(?=.*[a-z]).{8,}$', value): raise BadRequest("Please provide a valid password")


def _validate_project(data):
    for key, value in data.items():
        # ensure keys have values
        if not value: raise BadRequest("{} is lacking. It is a required field".format(key))
        if key == "owner":
            if len(value) < 5: 
                raise BadRequest("The {} provided is too short".format(key))
            elif len(value) > 15: 
                raise BadRequest("The {} provided is too long".format(key))
            else: 
                for i in value:
                    if i not in string.ascii_letters: 
                        raise BadRequest("{} cannot have non-alphabetic characters.".format(key))
