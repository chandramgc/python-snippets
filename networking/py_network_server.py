#!/usr/bin/python3

import socket

size = 512
host = 'localhost'
port = 9898

# Family = Internet, type = stream socket mean TCP
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# We have a socket, we need to bind to an IP address and port
# to have a place to listen on
sock.bind((host, port))
sock.listen(5)
# We can store information about the other end
# once we accept the connectio attempt
c, addr = sock.accept()
data = c.recv(size)
if data:
  f = open("storage.dat", '+w')
  print("connection from: ", addr[0])
  f.write(addr[0])
  f.write(":")
  f.write(data.decode("utf-8"))
  f.close()
sock.close()


# Listen msg using nc command
# nc -l 5555
