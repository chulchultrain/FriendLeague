import os
import subprocess
import datetime
import time

#   League Util: Exists as a place for utility functions that have a place in many scripts
#
#
#
#


#   get_current_timestamp is necessary because RIOT api doesnt return the normal UNIX timestamp
#   but rather a timestamp based off of milliseconds(rather than seconds).
#   So had to take UNIX timestamp and multiply by 1000
#
#
#
def get_current_timestamp():
    res = long(time.time() * 1000)
    return res
