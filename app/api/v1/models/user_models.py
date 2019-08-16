from flask import send_file, send_from_directory, jsonify, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from .base_model import BaseModel


class UserModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, username="", first_name="",last_name="", ek_number="", email="", 
                phone_number="", password="", user_level=""):
        """initialize the user model"""
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.ek_number = ek_number
        self.email = email
        self.phone_number = phone_number
        self.password = generate_password_hash(password)
        self.user_level = user_level
        self.db = init_db()

    def download(self, f):
        try:
            return request.host_url+url_for('static', filename='profile/'+f)
        except FileNotFoundError:
            return "name" 
    

    def get_users(self):
        dbconn = init_db()
        curr = dbconn.cursor()
        curr.execute("""SELECT username, first_name, last_name, ek_number, email, phone_number, profile, user_level FROM users;""")
        data = curr.fetchall()
        resp = []
        curr.close()

        for i, items in enumerate(data):
            username, first_name, last_name, ek_number, email, phone_number, profile, user_level = items
            users = dict(
                Profile= "<img class='rounded-circle' src='{}' alt=''>".format("https://source.unsplash.com/fn_BT9fwg_E/60x60"),
                Username="<a href='profile.html?username={}'> {} </i></a>".format(username, username),
                First_Name=first_name,
                Last_Name=last_name,
                EK_Number=ek_number,
                Email=email,
                Phone=phone_number,
                User_Level=int(user_level)
            )
            resp.append(users)
        return resp

    def get_specific_user(self, username):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """SELECT username, first_name, last_name, ek_number, email, phone_number, position, profile, user_level FROM users WHERE username=%s """
        curr.execute(query, [username])
        data = curr.fetchone()
        curr.close()
        resp = []

        username, first_name, last_name, ek_number, email, phone_number, position, profile, user_level = data
        users = dict(
            username=username,
            first_name=first_name,
            last_name=last_name,
            ek_number=ek_number,
            email=email,
            phone_number=phone_number,
            position=position,
            profile=self.download(profile),
            user_level=int(user_level)
        )
        resp.append(users)
        return resp

    def save(self):
        """Add user details to the database"""
        user = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "ek_number": self.ek_number,
            "email": self.email,
            "phone_number": self.phone_number,
            "password": self.password,
            "user_level": self.user_level
        }
        database = self.db
        curr = database.cursor()
        query = """INSERT INTO users (username, first_name, last_name, ek_number, email, phone_number, password, user_level) \
                    VALUES (%(username)s, %(first_name)s, %(last_name)s, %(ek_number)s, %(email)s,\
                    %(phone_number)s, %(password)s, %(user_level)s );
                """
        curr.execute(query, user)
        database.commit()
        curr.close()
        return "Success"
