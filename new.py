import requests, datetime, os
from datetime import timedelta
from Mysql import create_connection, get_domains_list
from mysql.connector import MySQLConnection
from dotenv import load_dotenv

class Domain():
    def __init__(self,domain, exp_date) -> None:
        self.domain = domain
        if exp_date:
            self.exp_date = exp_date
    
    def get_exp_dates(self):
        api_key = os.getenv(f"TEMP_API_KEY")
        response = requests.get(f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={self.domain}&outputFormat=JSON")
        main_responce_dict = response.json()
        exp_date_time=main_responce_dict['WhoisRecord']['expiresDateNormalized']
        print(exp_date_time)
        self.exp_date = datetime.datetime.strptime(exp_date_time, '%Y-%m-%d %H:%M:%S UTC').date()
        return self
        
    
    def compare_dates(self) -> timedelta:
        now=datetime.datetime.now().date()
        if 'exp_date' not in vars(self).keys(): 
            self.get_exp_dates()
        return self.exp_date - now
    
    def updateDateInDatabase(self, db: MySQLConnection):
        try:
            date = self.exp_date.strftime("\'%y-%m-%d\'")
            cursor = db.cursor()
            cursor.execute(f"update domains SET date = {date} WHERE domain = \'{self.domain}\';")
            db.commit()
        finally:
            cursor.close()

def main():
    domains=[]
    load_dotenv()
    try:
        db=create_connection()
    
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

    finally:
        db.close()

if __name__ == "__main__":
    main() 