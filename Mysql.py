import mysql.connector, logging
logger = logging.getLogger(__name__)

def create_connection(host, user, password, database):
    try:
        logger.info("Trying to connect MySQL Database.")
        db = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            db = database
        )
        if 'db' in locals().keys():
            logger.info("Connected!")
            return db
        else:
            ConnectionError("Unable to connect To Database.")
    except ConnectionError as e:
        logger.error(e.args)
        

def get_domains_list(db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()
        cursor.execute("select id, domain, date, comments from domains;")
        return cursor.fetchall()
    finally:
        if 'cursor' in locals().keys():
            cursor.close()
