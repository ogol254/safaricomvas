from flask_restplus import Resource
from flask import send_file, send_from_directory, jsonify, url_for, request


from ..utils.serializers import FileDTO


api = FileDTO().api

n_file = FileDTO().n_file

@api.route("/<string:location>/<string:filename>")
class Files(Resource):

    @api.marshal_with(n_file, code=201)
    def get(self, location, filename):
        try:
            resp = { "files" : request.host_url+url_for('static', filename=location+'/'+filename)}
            return resp, 200

        except FileNotFoundError:
            return request.host_url+url_for('static', filename="profile/avater.png") 