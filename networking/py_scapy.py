#!/usr/bin/python

from scapy.all import *

frame = Ether(dst="")/IP(dst="")/TCP()/"This is my payload"

print(frame)
sendp(frame)
