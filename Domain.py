import requests, os
from mysql.connector import MySQLConnection
from datetime import timedelta, datetime
class Domain():
    def __init__(self,domain, exp_date: datetime) -> None:
        self.domain = domain
        if exp_date:
            self.exp_date = exp_date
    
    def get_exp_dates(self):
        try:
            api_key = os.getenv(f"API_KEY")
            response = requests.get(f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={self.domain}&outputFormat=JSON")
            main_responce_dict = response.json()
            exp_date_time=main_responce_dict['WhoisRecord']['expiresDateNormalized']
            print(exp_date_time)
            self.exp_date = datetime.strptime(exp_date_time, '%Y-%m-%d %H:%M:%S UTC').date()
            return self
        except Exception as e:
            print(f"Exception Thrown while calling API: {e}")
        
    
    def compare_dates(self) -> timedelta:
        now=datetime.now().date()
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
