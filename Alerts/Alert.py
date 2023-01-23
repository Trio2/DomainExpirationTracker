class Alert():
    def __init__(self, alert_name, sender, receivers,body,port) -> None:
        self.alert_name = alert_name
        self.sender=sender
        self.recivers=receivers
        self.body=body
        self.port=port

