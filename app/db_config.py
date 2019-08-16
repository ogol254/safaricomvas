from flask import current_app
from contextlib import closing
import mysql.connector as mysql
import os
from werkzeug.exceptions import ServiceUnavailable

# cnx = mysql.connector.connect(user="mcogol@myswl-database", password={your_password}, host="myswl-database.mysql.database.azure.com", port=3306, database={your_database}, ssl_ca={ca-cert filename}, ssl_verify_cert=true)

# user="mcogol@myswl-database", password="Masterabram1!", host="myswl-database.mysql.database.azure.com", port=3306, database="vas_assets")

def connection():
    try:
        conn = mysql.connect(user="mcogol@myswl-database", password="Masterabram1!", host="myswl-database.mysql.database.azure.com", port=3306, database="vas_assets")
        return conn
    except:
        raise ServiceUnavailable("OOPS!! We cannot reach the database server at the moment")


def init_db():
    """Set up the database to stode the user data
    """
    db_url = os.getenv('DATABASE_URL')
    conn = connection()
    cursor = conn.cursor()
    sql = current_app.open_resource('sql_tables.sql', mode='r')
    cursor.execute(sql.read(), multi=True)
    conn.commit()
    
    # with conn as con, con.cursor() as curr:
    #     sql = current_app.open_resource('sql_tables.sql', mode='r') 
    #     curr.execute(sql.read(), multi=True)
    #     con.commit()
    return conn


def init_test_db():
    conn = connection(os.getenv('DATABASE_TEST_URL'))
    destroy_db()
    with conn as conn, conn.cursor() as cursor:
        with current_app.open_resource('sql_tables.sql', mode='r') as sql:
            cursor.execute(sql.read())
        conn.commit()
        return conn


def destroy_db():
    conn = connection()
    curr = conn.cursor()
    blacklist = """DROP TABLE IF EXISTS blacklist CASCADE; """
    users = """DROP TABLE IF EXISTS users CASCADE; """
    queries = [blacklist, users]

    try:
        for query in queries:
            curr.execute(query)
        conn.commit()
    except:
        raise ServiceUnavailable("OOPS!! We cannot reach the database server at the moment")
