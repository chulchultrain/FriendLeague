import os
import subprocess
import datetime
import time
import pickle
import psycopg2
import league_conf
#   League Util: Exists as a place for utility functions that have a place in many scripts
#
#
#
#


def conn_postgre():
    conn = psycopg2.connect(host=league_conf.postgre_host,
    database=league_conf.postgre_db,
    user=league_conf.postgre_user,
    password=league_conf.postgre_pass)
    return conn

#load_pickled_map function
#loads a pickled map from the passed file name



def load_pickled_map(file):
    res = {}
    try:
        with open(file,'rb') as fin:
            res = pickle.load(fin)
    except Exception as e:
        print("Couldn't load pickled file")
        print(e)
        res = {}
    return res

#save_pickled_map function
#saves a map into a pickled file, given both the map structure and the file name

def save_pickled_map(file,m): #i feel like i need a try catch
    try:
        with open(file,'wb') as fout:
            pickle.dump(m,fout)
    except Exception as e:
        print("Couldn't write pickled file")
        print(e)
#   get_current_timestamp is necessary because RIOT api doesnt return the normal UNIX timestamp
#   but rather a timestamp based off of milliseconds(rather than seconds).
#   So had to take UNIX timestamp and multiply by 1000
#
#
#
def get_current_timestamp():
    res = time.time()
    return res

def dt_to_riot_timestamp(dt):
    timestamp = dt.timestamp()
    timestamp = int(timestamp * 1000)
    return timestamp

if __name__ == '__main__':
    print(get_current_timestamp() )
    conn_postgre()
