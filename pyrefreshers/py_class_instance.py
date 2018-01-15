#!/usr/bin/python3

class me:
  def __init__(self, foo):
    self.myvar = foo

  def getval(self):
    return self.myvar

  def setval(self, y):
    self.myvar = y

my1 = me("this")
my2 = me("who")
my3 = me("self")

x = my1.getval()
print(x)
x = my2.getval()
print(x)
my3.setval("testing")
x = my3.getval()
print(x)
