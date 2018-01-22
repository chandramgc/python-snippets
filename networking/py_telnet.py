#!/usr/bin/python3

import telnetlib, getpass

# user = getpass.getuser()
user = "girish" 
pw = getpass.getpass() 
host = "192.168.1.50" 

t = telnetlib.Telnet(host) 

try:
    t.read_until("login: ")
    t.write(user + '\n')
    t.read_until("Password: ")
    t.write(pw + '\n')
    t.read_until("~ $ ")
    t.write("ls\n")
    print(t.read_until("~ $ ")) 
except Exception as e:
    print(e) 
finally:
    t.close()
