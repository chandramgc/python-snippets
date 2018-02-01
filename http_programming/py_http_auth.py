#!/usr/bin/python3

import httplib2
import base64 
import string 

h = "localhost" 
u = "girish" 
p = "123456" 

authToken = base64.b64encode(bytes( ('%s:%s' % (u, p)).replace('\n', ''), "utf8" )) 
print(authToken) 

req = httplib2.HTTP(h) 
req.putrequest("GET", "/protected/index.html") 
req.putheader("Host", h) 
req.putheader("Authorization", "Basic %s" % authToken) 
req.endheaders() 
req.send("") 

statusCode, statusMsg, headers = req.getreply()

print("Response: ", statusMsg)
