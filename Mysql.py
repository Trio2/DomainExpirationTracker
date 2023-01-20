import mysql.connector, os
from dotenv import load_dotenv

def create_connection():
    load_dotenv()
    return mysql.connector.connect(
        host = os.getenv("HOST_SQL"),
        user = os.getenv("USER_SQL"),
        password = os.getenv("PASSWORD_SQL"),
        db = os.getenv("DB_SQL")
    )

def get_domains_list(db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()
        cursor.execute("select id, domain, date, comments from domains;")
        return cursor.fetchall()
    finally:
        cursor.close()


