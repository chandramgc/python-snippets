#!/usr/bin/python3

try:
  fhandle = open("myfile", "w")
  fhandle.write("This is some data to dump into the file")
  print("Wrote some data to the file")
except IOError as e:
  print("Exception caugth: Unable to write to myfile", e)
except Exception as e:
  print("Another error occurred ", e)
else:
  print("File written to successfully")
  fhandle.close()
