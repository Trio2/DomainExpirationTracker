import mysql.connector, os
from dotenv import load_dotenv

def create_connection(host, user, password, database):
    load_dotenv()
    return mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        db = database
    )

def get_domains_list(db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()
        cursor.execute("select id, domain, date, comments from domains;")
        return cursor.fetchall()
    finally:
        cursor.close()


