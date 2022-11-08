# SPM-G1T1
 

### To start up the project 
1. Start WAMP/MAMP
2. import the sql tables with php my admin
    1. backend/sql/createTables.sql
    2. backend/sql/insertDataSetA.sql
    3. backend/sql/insertDataSetB.sql
3. create a .env file in /backend/server/.env (see data below)
4. run the server /backend/server/flaskServer.py
5. run the frontend with live server /frontend/index.html
    1. alternatively, move the whole folder to /www. in WAMP/MAMP and run the run the frontend with WAMP/MAMP 

.env
DB_USERNAME = 'root'
DB_PASSWORD = ''

(or personal username and password for WAMP/MAMP)


To note:
from the index page, password is not required for all users
login and password management to be completed in further releases