#!/usr/bin/python3

import threading

class aThread(threading.Thread):
  def __init__(self, num, val):
    threading.Thread.__init__(self)
    self.threadNum = num
    self.loopCount = val

  def run(self):
    print("Starting run: ", self.threadNum)
    myfunc(self.threadNum, self.loopCount)
    
def myfunc(num, val):
  count=0
  while count < val:
    print(num, " : ", val*count)
    count=count+1


t1=aThread(1, 15)
t2=aThread(2, 20)
t3=aThread(3, 25)
t4=aThread(4, 30)

# Starting threads
t1.start()
t2.start()
t3.start()
t4.start()

# Append them to a collection
threads = []
threads.append(t1)
threads.append(t2)
threads.append(t3)
threads.append(t4)

# Wait for all threads to complete by entering them
for t in threads:
  t.join()
