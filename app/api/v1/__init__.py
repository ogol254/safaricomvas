"""
This module sets up the users resource
Authored by: Ogol
"""
from flask_restplus import Api
from flask import Blueprint
from werkzeug.exceptions import NotFound

version_one = Blueprint('version1', __name__, url_prefix="/api/v1")

from .views.auth import api as auth_ns
from .views.users import api as user_ns
from .views.projects import api as j_ns
from .views.files import api as files
from .views.projectfiles import api as projectfiles
from .views.assets import api as assets
from .views.statistics import api as stats
# from .views.records import api as record_ns
# from .views.comments import api as cm_ns
# from .views.facilities import api as f_ns
# from .views.bio import api as bio_ns


api = Api(version_one,
          title='VAS ASSETS API',
          version='1.0',
          description="")

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(user_ns, path="/users")
api.add_namespace(j_ns, path="/projects")
api.add_namespace(files, path="/resource")

api.add_namespace(projectfiles, path="/projects")
api.add_namespace(assets, path="/projects")

api.add_namespace(stats, path="/stats")
# api.add_namespace(record_ns, path="/records")
# api.add_namespace(cm_ns, path="/records/<int:record_id>/comment")
# api.add_namespace(bio_ns, path="/users/<int:id_number>/bio")
