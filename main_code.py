import os
from Domain import Domain
from Mysql import create_connection, get_domains_list
from dotenv import load_dotenv

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
            if domain[2] == None:
                dom = Domain(domain[1],None)
                dom.get_exp_dates()
                dom.updateDateInDatabase(db)
            else: 
                dom=Domain(domain[1],domain[2])
            domains.append(dom)
            if dom.compare_dates().days < 30: #Do Date Compare
                print("This is email send function")
    except Exception as e:
        print(e) #Write more spesific exception and adopt logging methods
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    main() 
