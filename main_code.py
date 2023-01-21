import os , logging, logging.config 
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
    domains=[]
    try:
        db=create_connection(
            host = os.getenv("HOST_SQL"),
            user = os.getenv("USER_SQL"),
            password = os.getenv("PASSWORD_SQL"),
            database = os.getenv("DB_SQL")
        )
        for domain in get_domains_list(db): 
            dom = Domain(domain,db)            
            domains.append(dom)  

        #TODO add email and sms logic        
          
    except Exception as e:
        print(e) #Write more spesific exception and adopt logging methods
    finally:
        if 'db' in locals().keys():
            db.close()

if __name__ == "__main__":
    main() 