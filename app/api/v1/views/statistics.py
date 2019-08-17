import os
import re
import json
import string
import werkzeug
from random import randint
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden, Conflict

from flask_restplus import Resource, reqparse
from flask import jsonify, make_response, request, g, jsonify, redirect, url_for

from ..utils.serializers import StatisticsDTO
from ..models.statistics_model import StatisticsModel 
from ..utils.auth_validation import auth_required

api = StatisticsDTO().api

@api.route("/db")
class Statistics(Resource):
    
    @auth_required
    def get(self):
        return StatisticsModel().get_quantities()
        
