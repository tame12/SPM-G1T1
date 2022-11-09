# SPM-G1T1
 

### To start up the project 
1. Start WAMP/MAMP
2. import the sql tables with php my admin in this order
    1. backend/sql/createTables.sql 
    2. backend/sql/insertDataSetA.sql (our own test data)
    3. backend/sql/insertDataSetB.sql (test data given to us on elearn)
3. create a .env file in /backend/server/.env (see data below)
4. run the server /backend/server/flaskServer.py
5. run the frontend with live server /frontend/index.html
    1. alternatively, move the whole folder to /www. in WAMP/MAMP and run the run the frontend with WAMP/MAMP 

.env
DB_USERNAME = \<insert your php my admin DB username\>

DB_PASSWORD = \<insert your php my admin DB password\>

To note:


when login, choose the role you want to view the pages for

choose any email from the dropdown (no need password)

click login

login and password management to be completed in further releases