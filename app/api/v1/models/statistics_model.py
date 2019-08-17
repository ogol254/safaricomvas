from flask import send_file, send_from_directory, jsonify, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class StatisticsModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self):
        """initialize the user model"""
        self.db = init_db()
        self.cur = self.db.cursor()

    def get_quantities(self):
        self.cur.execute("""select count(*) from users """ )
        users = self.cur.fetchone()[0]
        self.cur.execute("""select count(*) from projects """ )
        projects = self.cur.fetchone()[0]
        self.cur.execute("""select count(*) from assets """ )
        assets = self.cur.fetchone()[0]
        self.cur.execute("""select count(*) from files """ )
        documents = self.cur.fetchone()[0]
        return { "projects" : projects, "users" : users,"assets" : assets, "documents" : documents }

