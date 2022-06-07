#!bin/usr/env python3

import subprocess
import json
from datetime import date
import psycopg2 #Need to install with pip!
import hashlib

#Sebastian Tramontana
#6/7/2022
#
# This script reads a message from the aws sqs queue, parses the fields from the 'body',
# hashes the device_id and ip fields, and then inserts the fields as a row into the user_logins table.
#
# Note: This script only performs the above action once; it does not loop.


#Retrieve data from sqs queue:
#Command used: awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
aws_cmd_list = ["awslocal", "sqs", "receive-message", "--queue-url", "http://localhost:4566/000000000000/login-queue"]

#Runs aws command using subprocess.run:
sqs_res = subprocess.run(aws_cmd_list, capture_output=True, text=True).stdout

#Parses Json response into dictionary:
sqs_json = json.loads(sqs_res)
#Retrieves "Body" of message:
sqs_body = json.loads(sqs_json["Messages"][0]["Body"])

#Retrieve each field from the body:

user_id = sqs_body["user_id"]

#NOTE: In order to properly insert app version into database,
# I had to remove the dots.  Type of app_version in DDL is 'integer'.
app_version = sqs_body["app_version"]
app_version = app_version.replace(".", "")

device_type = sqs_body["device_type"]
ip = sqs_body["ip"]
locale = sqs_body["locale"]
device_id = sqs_body["device_id"]

#create date for postgres entry:
create_date = date.today()


#Mask the device_id and ip fields:
#
#I decided to use sha256 hash to mask the data.
ip = hashlib.sha256(ip.encode()).hexdigest()
device_id = hashlib.sha256(device_id.encode()).hexdigest()




#Connecting to postgres in docker container:
conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="postgres",
    port=5432
)

#This makes it so we could execute commands in the db:
cur = conn.cursor()

#Execute db command:
cur.execute("INSERT INTO user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
(user_id, device_type, ip, device_id, locale, app_version, create_date))



#Commit changes to db
conn.commit()

#Close communication with db
cur.close()
conn.close()

