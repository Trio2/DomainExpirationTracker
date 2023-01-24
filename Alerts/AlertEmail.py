import smtplib ,os, random
from email.message import EmailMessage
from datetime import datetime
from Alerts.Alert import Alert

class AlertEmail(Alert):
    def __init__(self, sender, receivers, domainName, exp_in_days) -> None:
        super().__init__(sender, receivers, domainName, exp_in_days)    

    def execute(self):   
        try:
            msg = EmailMessage()
            msg['From'] = self.sender
            msg['To'] = self.receivers
            msg['subject'] = f'{self.domainName}: Expires in {self.exp_in_days}'
            msg.set_content(f'Email content goes here')
            msg['Message-ID'] = datetime.now().strftime("%Y%m%d%H%M%S") +"." + str(random.randint(1000,9999)) + f'EC11E6F@{os.getenv("SMTP_HOST")}'
            smtp = smtplib.SMTP(os.getenv("SMTP_HOST"))
            if type(self.receivers) == 'list':
                for i in self.receivers:
                    smtp.sendmail(self.sender, i, msg.as_string())
            else:
                smtp.sendmail(self.sender, self.receivers, msg.as_string())
        except Exception as e:
            print(e)
        finally:
            if 'smtp' in locals().keys():
                smtp.close()
        