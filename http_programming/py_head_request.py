#!/usr/bin/python
import httplib 
host = "localhost" 
req = httplib.HTTP(host) 
req.putrequest("HEAD", "/") 
req.putheader("Host", host) 
req.endheaders() 
req.send("") 
statusCode, statusMsg, headers = req.getreply()
print("Status: ", statusCode)
