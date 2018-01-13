#!/usr/bin/python3

import pymysql

# Open database connection
db = pymysql.connect("localhost","root","root","mydatabase" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to DELETE required records
sql = "SELECT * FROM product1tb"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists
   results = cursor.fetchall()
   # Print fetched results
   for row in results:
      print(row)
   cursor.close()
except:
   print("Error: Unable to fetch data")   

# disconnect from server
db.close()
