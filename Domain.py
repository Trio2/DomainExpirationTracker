import requests, os, logging
from mysql.connector import MySQLConnection
from datetime import timedelta, datetime
from Alerts.AlertEmail import AlertEmail

logger = logging.getLogger(__name__)

class Domain():
    def __init__(self, domain: tuple, db) -> None:
        self.domain = domain[1]
        if domain[2] != None:
            self.exp_date = domain[2]
        else:
            self.get_exp_dates().updateDateInDatabase(db)
    
    def get_exp_dates(self):
        try:
            logger.info("Trying to query from API")
            api_key = os.getenv(f"API_KEY")
            response = requests.get(f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={self.domain}&outputFormat=JSON")
            self.exp_date = datetime.strptime(
                response.json()['WhoisRecord']['expiresDateNormalized'], 
                '%Y-%m-%d %H:%M:%S UTC'
                ).date()
            logger.info(f"Querying date for {self.domain} was successfull the expiration date is: {self.exp_date}")
            return self
        except Exception as e:
            logger.error(f"Exception Thrown while calling API.")
            logger.exception(e)     
    
    def compare_dates(self) -> timedelta:
        try:
            now=datetime.now().date()
            if 'exp_date' not in vars(self).keys(): 
                self.get_exp_dates()
            return self.exp_date - now
        except Exception as e:
            logger.error(f'exception thrown while comparing dates from domain {self.domain}')
            logger.exception(e)
    
    def updateDateInDatabase(self, db: MySQLConnection):
        try:
            date = self.exp_date.strftime("\'%y-%m-%d\'")
            cursor = db.cursor()
            cursor.execute(f"update domains SET date = {date} WHERE domain = \'{self.domain}\';")
            db.commit()
        except Exception as e:
            logger.error(f"unable to update the date {self.exp_date} for domain: {self.domain}")
        finally:
            if 'cursor' in locals().keys():
                cursor.close()
            return self
            
    def alretNeeded(self) -> bool:
        return self.compare_dates().days < int(os.getenv("ALERT_IN_DAYS"))
    
    def createEmail(self) -> AlertEmail:
        return AlertEmail(
            sender = os.getenv("SMTP_FROM"),
            receivers = os.getenv("SMTP_TO"),
            domainName = self.domain,
            exp_in_days = self.compare_dates().days
        )

