from flask import send_file, send_from_directory, jsonify, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class ProjectModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, _id="", name="", description="", default_owner="", start_date="", 
                 owner="", created_by="", user_level=""):
        """initialize the user model"""
        self._id = _id
        self.name = name
        self.description = description
        self.default_owner = default_owner
        self.start_date = start_date
        self.owner = owner
        self.created_by = created_by
        self.db = init_db()
        self.cur = self.db.cursor()
    

    def get_projects(self):
        query = """SELECT _id, name, default_owner, start_date, owner
                  FROM projects WHERE status=1 ORDER BY created_at DESC """ 
        self.cur.execute(query)
        data = self.cur.fetchall()
        resp = []
        self.cur.close()

        for i, items in enumerate(data):
            _id, name, default_owner, start_date, owner  = items
            projects = {
                "_id" : int(_id),
                "Name" : name,
                "Department" : default_owner,
                "start_date" : str(start_date),
                "Assignee" : owner,
                "Action" : "<a href='edit_project.html?id={}'><i class='fas fa-fw fa-edit'></i></a>   <a href='view_project.html?id={}'><i class='fas fa-fw fa-bullseye'></i></a>".format(_id, _id)
            }
            resp.append(projects)
        return resp


    def get_specific_project(self, _id):
        query = """SELECT _id, name, description, default_owner, start_date, owner, created_by, status, created_at FROM projects WHERE _id=%s """
        self.cur.execute(query, [_id])
        data = self.cur.fetchone()
        self.cur.close()
        resp = []

        _id, name, description, default_owner, start_date, owner, created_by, status, created_at = data
        projects = dict(
            _id=int(_id),
            name=name,
            description=description,
            default_owner=default_owner,
            start_date=str(start_date),
            owner=owner,
            created_by=created_by,
            status=int(status),
            created_at=str(created_at)
        )
        resp.append(projects)
        return resp

    def save(self):
        """Add user details to the database"""
        user = {
            "_id": self._id,
            "name": self.name,
            "description": self.description,
            "default_owner": self.default_owner,
            "start_date": self.start_date,
            "owner": self.owner,
            "created_by": self.created_by
        }
        query = """INSERT INTO projects (_id, name, description, default_owner, start_date, owner, created_by) \
                    VALUES (%(_id)s, %(name)s, %(description)s, %(default_owner)s, %(start_date)s,\
                    %(owner)s, %(created_by)s);
                """
        self.cur.execute(query, user)
        self.db.commit()
        self.cur.close()
        return "Success"

    def get_projects_user(self, username, limit, offset):
        query = """SELECT _id, name, description, default_owner, start_date, owner , status, created_at 
                  FROM projects WHERE created_by ='%s' ORDER BY created_at DESC LIMIT %s OFFSET %s  """ %(username, limit, offset)
        self.cur.execute(query)
        data = self.cur.fetchall()
        resp = []
        self.cur.close()

        for i, items in enumerate(data):
            _id, name, description, default_owner, start_date, owner, status, created_at  = items
            projects = dict(
                _id=int(_id),
                name=name,
                description=description,
                default_owner=default_owner,
                start_date=str(start_date),
                owner=owner,
                status=int(status),
                created_at=str(created_at)
            )
            resp.append(projects)
        return resp
