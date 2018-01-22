#!/usr/bin/python3
import ftplib 

f = ftplib.FTP("192.162.1.127") 

try:
    f.login("girish", "123456")
    print(f.getwelcome())
    f.delete("myfile")
    print(f.dir())
    f.set_pasv(1)
    f.storbinary("STOR myfile", open("myfile", "rb"))
    print(f.dir()) 
except Exception as e:
    print("Exception: ", e) 
finally:
    f.close()
