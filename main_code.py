import os , logging, logging.config, queue
from Domain import Domain
from Mysql import create_connection, get_domains_list
from dotenv import load_dotenv
from datetime import datetime

logging.basicConfig(
    filename=f'logs/Testlog-{datetime.now().strftime("%d-%m-%Y--%H.%M.%S")}.log',
    format='%(filename)s-%(levelname)s-%(message)s',
    level=logging.INFO
)

def main():
    load_dotenv()
    domains= queue.Queue()
    try:
        db=create_connection(
            host = os.getenv("HOST_SQL"),
            user = os.getenv("USER_SQL"),
            password = os.getenv("PASSWORD_SQL"),
            database = os.getenv("DB_SQL")
        )
        for domain in get_domains_list(db): 
            dom = Domain(domain, db)            
            domains.put(dom) if dom.alretNeeded() else None
        while not domains.empty():
            domains.get().createEmail().execute()

    except Exception as e:
        logging.error(f"Exception Thrown!")
        logging.exception(e) 
    finally:
        if 'db' in locals().keys():
            db.close()

if __name__ == "__main__":
    main() 