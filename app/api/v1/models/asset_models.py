from flask import send_file, send_from_directory, jsonify, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class AssetsModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, _id="", project_id="", type="", hostname="", interface1="", 
                 interface2="", interface3="", peer_systems="", description=""):
        """initialize the user model"""
        self._id = _id
        self.project_id = project_id
        self.type = type
        self.hostname = hostname
        self.interface1 = interface1
        self.interface2 = interface2
        self.interface3 = interface3
        self.peer_system = peer_systems
        self.description = description
        self.db = init_db()
        self.cur = self.db.cursor()
    

    def get_assets(self):
        query = """SELECT _id, project_id, type, hostname, interface1, interface2, interface3, peer_system, description, created_at 
                  FROM assets WHERE status=0 ORDER BY created_at DESC """
        self.cur.execute(query)
        data = self.cur.fetchall()
        resp = []
        self.cur.close()

        for i, items in enumerate(data):
            _id, project_id, type, hostname, interface1, interface2, interface3, peer_systems, description, created_at  = items
            assets = dict(
                _id=int(_id),
                project_id=int(project_id),
                type=type,
                hostname=hostname,
                interface1=interface1,
                interface2=interface2,
                interface3=interface3,
                peer_systems=peer_systems,
                description = description,
                created_at=str(created_at)
            )
            resp.append(assets)
        return resp

    def get_assets_projects(self, project_id):
        query = """SELECT _id, type, hostname, interface1, interface2, interface3, peer_system, description 
                  FROM assets WHERE project_id=%s ORDER BY created_at DESC  """ %(project_id)
        self.cur.execute(query)
        data = self.cur.fetchall()
        resp = []
        self.cur.close()

        for i, items in enumerate(data):
            _id, type, hostname, interface1, interface2, interface3, peer_systems, description  = items
            assets = dict(
                _id=int(_id),
                type=type,
                hostname=hostname,
                interface1=interface1,
                interface2=interface2,
                interface3=interface3,
                peer_systems=peer_systems,
                description = description
            )
            resp.append(assets)
        return resp

    def get_specific_asset(self, _id):
        query = """SELECT _id, project_id, type, hostname, interface1, interface2, interface3, peer_system, description, status, created_at FROM assets WHERE _id=%s """
        self.cur.execute(query, [_id])
        data = self.cur.fetchone()
        self.cur.close()
        resp = []

        _id, project_id, type, hostname, interface1, interface2, interface3, peer_systems, description, status, created_at = data
        assets = dict(
            _id=int(_id),
            project_id=project_id,
            type=type,
            hostname=hostname,
            interface1=interface1,
            interface2=interface2,
            interface3=interface3,
            peer_systems=peer_systems,
            description = description,
            status=int(status),
            created_at=str(created_at)
        )
        resp.append(assets)
        return resp

    def save(self):
        """Add user details to the database"""
        user = {
            "_id": self._id,
            "project_id": self.project_id,
            "type": self.type,
            "hostname": self.hostname,
            "interface1": self.interface1,
            "interface2": self.interface2,
            "interface3": self.interface3,
            "peer_system": self.peer_system,
            "description": self.description
        }
        query = """INSERT INTO assets (_id, project_id, type, hostname, interface1, interface2, interface3, peer_system, description) \
                    VALUES (%(_id)s, %(project_id)s, %(type)s, %(hostname)s, %(interface1)s,\
                    %(interface2)s, %(interface3)s, %(peer_system)s,  %(description)s);
                """
        self.cur.execute(query, user)
        self.db.commit()
        self.cur.close()
        return "Success"