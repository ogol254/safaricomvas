    
import os
import re

from flask import request, g, send_from_directory
# from flask_restful import reqparse, abort, Resource, fields, marshal_with
from werkzeug import secure_filename

# from api.models import File, Folder
# from api.utils.decorators import login_required, validate_user, belongs_to_user

BASE_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)

print(BASE_DIR)
