class Alert():
    def __init__(self, sender, receivers, domainName, exp_in_days) -> None:
        self.sender=sender
        self.receivers=receivers
        self.domainName=domainName
        self.exp_in_days=exp_in_days

