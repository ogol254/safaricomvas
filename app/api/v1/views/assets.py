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

from ..utils.email import Email
from ..utils.serializers import AssetsDTO
from ..models.asset_models import AssetsModel 
from ..utils.auth_validation import auth_required


api = AssetsDTO().api
n_asset = AssetsDTO().n_asset
n_asset_resp = AssetsDTO().n_asset_resp


def get_asset_id(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    num_id = randint(range_start, range_end)
    if AssetsModel().check_exists(table="assets", field="_id", data=num_id) == False:return num_id
    else: get_asset_id(5)

########################################################################## POST AND GET ASSETS #########################################################################################

@api.route("/<int:project_id>/assets")
class Assets(Resource):
    @api.marshal_with(n_asset_resp, code=201)
    @api.expect(n_asset, validate=True)
    @auth_required
    def post(self, project_id):
        if AssetsModel().check_exists("projects", "_id", project_id) == True:
            req_data = request.data.decode().replace("'", '"')
            if not req_data:
                raise BadRequest("Provide data in the request")
            body = json.loads(req_data)
            try:
                typee = body['type'].strip()
                hostname = body['hostname'].strip()
                interface1 = body['interface1'].strip()
                interface2 = body['interface2'].strip()
                interface3 = body['interface3'].strip()
                peer_system = body['peer_system'].strip()
                description = body['description'].strip()
            except (KeyError, IndexError) as e:
                raise BadRequest

            asset_data = {
                "_id": get_asset_id(5),
                "project_id": project_id,
                "type": typee,
                "hostname": hostname,
                "interface1": interface1,
                "interface2": interface2,
                "interface3": interface3,
                "peer_systems": peer_system,
                "description": description
            }
            # _validate_asset(asset_data)
            a = AssetsModel(**asset_data)
            resp = a.save()
            respn = {
                "message": "Successfully created",
            }
            return respn, 201
        else:
            raise NotFound("No such project in our record")

    @auth_required
    def get(self, project_id):
        if AssetsModel().check_exists("projects", "_id", project_id) == True:
            resp = AssetsModel().get_assets_projects(project_id)
            return resp, 200
        else:
            raise NotFound("No such asset in our record")

########################################################################## ______________ #########################################################################################

@api.route("/assets")
class AssetSpecific(Resource):

    @auth_required
    def delete(self):
        resp = []
        data = request.json["assets"]
        for i in data:
            if AssetsModel().check_exists("assets", "_id", i) == True:
                AssetsModel().update_item(table="assets",field="status",data=1,item_field="_id",item_id=i)
                resp.append({"message" : "Success"})
            else:
                resp.append({"message" : "No asset with id of {} in our directory".format(i)})

        respn = {
            "message" : "Deletion status of the selected assets",
            "UUID" : resp
        }
        return respn, 200

    @auth_required
    def get(self):

        resp = AssetsModel().get_assets()
        assets = {
            "quantity" : len(resp),
            "assets": resp
        }
        return resp, 200
        