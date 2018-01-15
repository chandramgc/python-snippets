#!/usr/bin/python3

import os
from subprocess import call

# Use the os interface to get access to system information
print(os.getcwd())
print(os.getuid())
print(os.getenv("PATH"))

# Using System
os.system("ls -la")

# Using Call
inputValue = input("Hit enter")
call(["ls", "-la"])
