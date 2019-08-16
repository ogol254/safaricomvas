from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class AuthModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, username="", password=""):
        """initialize the user model"""
        self.username = username
        self.password = generate_password_hash(password)
        self.db = init_db()

    def logout_user(self, token):
        """This function logs out a user by adding thei token to the blacklist table"""
        curr = self.db.cursor()
        query = """
                INSERT INTO blacklist (tokens) VALUES (%(tokens)s);
                """
        inputs = {"tokens": token}
        curr.execute(query, inputs)
        self.db.commit()
        curr.close()
