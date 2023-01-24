# Domain Expiration Tracker

### Project Goal: 
- Reading a list of domains from DB.
- Using API to query the expiration date of the domain.
- Alerting the User via preconfigured Email / SMS settings.

### Requirements:
#### pip install:
- dotenv
- requests
- mysql-connector

#### .env file with the folowing structure:

    #MySQL
    HOST_SQL=sql.server.com
    USER_SQL=sql-user
    PASSWORD_SQL=sql-password
    DB_SQL=sql-db-name

    #www.whoisxmlapi.com API KEY
    API_KEY=whois-api-key

    #SMTP
    SMTP_HOST=smtp.host.com
    SMTP_FROM=mail@from.com
    SMTP_TO=mail@to.com
    
    #Days to Alert
    ALERT_IN_DAYS=120


### Road Map and issues will be managed in the issues section of the repository.




