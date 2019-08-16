import os
import re
import json
import werkzeug
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden, Conflict

from flask_restplus import Resource
from flask import jsonify, make_response, request, g, jsonify, redirect, url_for

from ..utils.email import Email
from ..utils.serializers import ProjectFileDTO
from ..models.file_models import ProjectFilesModel 
from ..utils.auth_validation import auth_required, _validate_project


api = ProjectFileDTO().api
n_file = ProjectFileDTO().n_file
n_file_resp = ProjectFileDTO().n_file_resp


APP_ROOT = "C:\\Users\\aogol\\Desktop\\asset"
ALLOWED_EXTENSIONS = set(['pdf', 'docx', 'pptx', 'xlsx', 'pub', '.png'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



########################################################################## POST AND GET PROJECTS #########################################################################################

@api.route("/<int:project_id>/document")
class ProjectFiles(Resource):
    """This class collects the methods for the auth/signin method"""

    @auth_required
    # @api.marshal_with(n_file_resp, code=201)
    def post(self, project_id):
        resp = []
        target = os.path.join(APP_ROOT, 'files/documents')
        if not os.path.isdir(target):
            os.mkdir(target)

        name = request.form['name']
        description = request.form['description']
        links = request.files.getlist('document')

        if ProjectFilesModel().check_exists("projects", "_id", project_id) == True:
            for link in links:
                if link.filename == '':
                    resp.append({ "message": " Error getting the file "})
                else:
                    
                        if link and allowed_file(link.filename):
                            destination = "/".join([target, link.filename])
                            link.save(destination)
                            filedata = {
                                "project_id": project_id,
                                "name": name,
                                "description": description,
                                "link": link.filename,
                                "created_by": g.user
                            }
                            f = ProjectFilesModel(**filedata)
                            f.save()
                            image = { "message": "{} Successfully saved".format(link.filename) }
                            resp.append(image)
                        else:
                            resp.append({ "message": "{} Not saved, Allowed file types are .pdf, .docx, .pptx, .xlsx and .pub".format(link.filename)})
        else: 
            resp.append({"message" :"No such project in our record"})                   
        
        respn = { "message": " Upload status update", "Uplaod data" : resp }
        return respn, 201            


    @auth_required
    def get(self, project_id):
        if ProjectFilesModel().check_exists("projects", "_id", project_id) == True:

            resp = ProjectFilesModel().get_all_files_project(project_id)
            return resp, 200
        else:
            return {"message" :"No such project in our record"}


@api.route("/documents")
class FileOperation(Resource):

    @auth_required
    def delete(self):
        resp = []
        data = request.json["documents"]
        for i in data:
            if ProjectFilesModel().check_exists("files", "_id", i) == True:
                ProjectFilesModel().update_item(table="files",field="status",data=1,item_field="_id",item_id=i)
                resp.append({"message" : "Success"})
            else:
                # return {"message" : "No such file in our directory"}
                resp.append({"message" : "No file with id of {} in our directory".format(i)})

        respn = {
            "message" : "Deletion status of the selected files",
            "UUID" : resp
        }
        return respn, 200

    @auth_required
    def get(self):
        resp = ProjectFilesModel().get_all_files()
        return resp, 200
      