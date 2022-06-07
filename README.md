# Data Engineering Take Home #
# Details: #
The language I decided to use was python3.  This way, I was able to use
psycopg2 to connect with the postgres DB.  In order to mask the required fields, I used a sha256 hash.  The script to run is ```read_sqs.py```; I will go into more details below on how to install the required packages, and how to run.

## How to install required packages (beyond those already mentioned in assignment description):
1. psycopg2: Do ```pip install psycopg2```.  Here is the link to the site with the documentation: https://pypi.org/project/psycopg2/.

## How to run:
1. Make sure you are in the 'data-engineering-take-home' directory.  This will be the home directory from here on.
2. Run ```make start```.  This may take a bit of time.
3. To run the script, simply run ```python3 read_sqs.py```.
4. If you would like to see the results in the database, connect to the data base with ```psql -d postgres -U postgres  -p 5432 -h localhost -W```.  From there, run
the sql statement: ```SELECT * FROM user_logins;```.  You should then be able to see the row that was inserted into the table.

