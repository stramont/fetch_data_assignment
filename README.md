# Data Engineering Take Home #
# Details: #
The language I decided to use was python3.  This way, I was able to use
psycopg2 to connect with the postgres DB.  In order to mask the required fields, I used a sha256 hash.  The script to run is ```read_sqs.py```; I will go into more details below on how to install the required packages, and how to run.

## How to install required packages (beyond those already mentioned in assignment description):
1. psycopg2: Do ```pip install psycopg2```.  Here is the link to the site with the documentation: https://pypi.org/project/psycopg2/.

## How to run:
1. Make sure you are in the home directory of this repository.
2. Run ```make start```.  This may take a bit of time.
3. To run the script, simply run ```python3 read_sqs.py```.
4. If you would like to see the results in the database, connect to the data base with ```psql -d postgres -U postgres  -p 5432 -h localhost -W```.  From there, run
the sql statement: ```SELECT * FROM user_logins;```.  You should then be able to see the row that was inserted into the table.


## Notes:
1. When retrieving the messages from the sqs queue, the data in the "app_version" field looked like this: ```2.3.0```.  However, datatype of "app_version" in the DDL was of type integer, so in order to fit the app_version into the table, I just removed the dots, so 2.3.0 became 230.  
2. I assumed that the "create_date" column in the db refers to the date that the row is inserted into the table. 
3. I did not include a loop in this script that reads all the records from the queue.  To be honest, I forgot that only 100 records were written to the queue (per the project description), so maybe this is something that I should have done, but while I was working on this, I was thinking that there were an unlimited amount of records coming into the queue, so maybe the best way to handle this data would be just to loop the script itself.  

But if I were to include code to retrieve all 100 records, I would just loop lines 20-28, storing each json into a list.  Then I would loop line 70 (the sql insert) for each record.  Maybe this isn't necessary at all, but I'm just thinking off the top of my head.

