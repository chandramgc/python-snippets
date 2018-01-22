#!/usr/bin/python3

import poplib, imaplib, getpass 

p = poplib.POP3("192.168.1.127", 110)
# p = poplib.POP3_SSL("172.30.42.126", 995)

print(p.getwelcome()) 
p.user("giris") 
p.pass_("123456") 

print(p.list()) 

p.quit() 

i = imaplib.IMAP4("192.168.1.127", 143)

# i.login(getpass.getuser(), getpass.getpass_())
i.login("ric", "P4ssw0rd!") 
i.select() 
t, l = i.list() 
print("Response code: ", t) 
print(l) 

t, ids = i.search(None, "ALL") 
print("Response code: ", t) 
print(ids) 
t, msg = i.fetch('5', "(UID BODY[TEXT])")

#  store messages on the server 
#  i.store()
print(msg) 
i.close() 
i.logout()
