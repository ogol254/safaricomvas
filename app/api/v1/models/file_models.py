from flask import send_file, send_from_directory, jsonify, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class ProjectFilesModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, project_id="", name="", description="", link="", created_by=""):
        self.project_id=project_id
        self.name = name
        self.description = description
        self.link = link
        self.created_by = created_by
        self.db = init_db()
        self.cur = self.db.cursor()

    def download(self, f):
        try:
            return request.host_url+url_for('static', filename='documents/'+f)
        except FileNotFoundError:
            return "name" 

    def get_all_files(self):
        query = """SELECT _id, project_id, name, description, link, created_by, created_at 
                  FROM files WHERE status=0 ORDER BY created_at DESC  """
        self.cur.execute(query)
        data = self.cur.fetchall()
        resp = []
        self.cur.close()

        for i, items in enumerate(data):
            _id, project_id, name, description, link, created_by, created_at  = items
            files = dict(
                _id=int(_id),
                project_id=int(project_id),
                name=name,
                description=description,
                link=self.download(link),
                created_by=created_by,
                created_at=str(created_at)
            )
            resp.append(files)
        return resp

    def get_all_files_project(self, project_id):
        query = """SELECT _id, name, description, link, created_by FROM files
                   WHERE project_id=%s AND status=0 ORDER BY created_at DESC """ %(project_id)
        self.cur.execute(query)
        data = self.cur.fetchall()
        resp = []
        self.cur.close()

        for i, items in enumerate(data):
            _id, name, description, link, created_by  = items
            files = dict(
                    _id=int(_id),
                    name=name,
                    description=description,
                    link="<a href='{}'>{}</a>".format(self.download(link), link),
                    created_by=created_by
                )
            resp.append(files)
        return resp

  
    def save(self):
        """Add user details to the database"""
        files = {
            "project_id" : self.project_id,
            "name": self.name,
            "description": self.description,
            "link": self.link,
            "created_by": self.created_by
        }
        query = """INSERT INTO files (project_id, name, description, link, created_by) \
                    VALUES (%(project_id)s, %(name)s, %(description)s, %(link)s, %(created_by)s);
                """
        self.cur.execute(query, files)
        self.db.commit()
        self.cur.close()
        return "Success"