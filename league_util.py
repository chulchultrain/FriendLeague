import os
import subprocess
import datetime
import time

#print(time.time())
#r = time.time() * 1000
#print(r)
#print(long(r))

def get_current_timestamp():
    res = long(time.time() * 1000)
    return res
