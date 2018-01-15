#!/usr/bin/python3

import pymysql
import sys
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
   # Print headers
   print("id	,	name	,	description	,	price")
   print("-----------------------------------------------------------")
   # Print fetched results
   for row in results:
      id = row[0]
      name = row[1]
      description = row[2]
      price = row[3]
      print(str(id) + "	,	" + name + "	,	" + description + "	,	" + str(price))
   cursor.close()
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise   

# disconnect from server
db.close()
