import smtplib ,os 
from email.message import EmailMessage
#import mysql.connector
#from Mysql import create_connection, get_domains_list
from Alerts.Alert import Alert

class AlertEmail(Alert):
    def __init__(self, alert_name, sender, receivers, body, port, subject) -> None:
        super().__init__(alert_name, sender, receivers, body, port)
        self.subject = subject
    

    def execute(self):   
        msg = """From: From Person <from@fromdomain.com>
                    To: To Person <to@todomain.com>
                    Subject: SMTP e-mail test

                    This is a test e-mail message.
                    """
        #msg['subject'] = 'this is the subject'
        #msg['From'] = self.sender
        #msg['To'] = self.recivers
        #msg.set_content('this is main body')
        smtp = smtplib.SMTP('18.132.30.147') 
        smtp.sendmail(self.sender, self.recivers, msg) 