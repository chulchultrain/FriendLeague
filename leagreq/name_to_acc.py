import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'FriendLeague.settings'
import leagreq.league_curl as league_curl
import league_conf
import utils.league_util as league_util
import pickle
import subprocess
import django
from django.conf import settings
if __name__ == '__main__':
    django.setup()
from django.db import models
from analytics.models import Account

#TODO: What should happen when 4XX error?
# account_data_from_name_refresh function
# low level function
# makes an explicit request to the Riot API for the desired account data
# given a summoner name
def account_id_from_name_refresh(name):
    account_data = league_curl.request('summoner',name)
    if account_data is None:
        raise RuntimeError("Couldn't retrieve data for the summoner name " + name)
    return account_data['accountId']

# account_data_from_name function
# Top Level function
# gets account data from a name argument
# input : name : summoner name : string
# output : account data : summonerDTO type from Riot API

def exists_already(account_id,cursor=None):
    try:
        Account.objects.get(account_id=account_id)
    except Account.DoesNotExist as e:
        print(e)
        return False
    return True

def insert_new_account(account_id,name,cursor):
    big_int_array = 'array[]::bigint[]'
    to_timestamp_0 = 'to_timestamp(0)'
    param_li = [account_id,name]
    try:
        acc = Account(account_id=account_id,name=name)
        acc.save()
        #stmt = 'insert into analytics_account values(%s,%s,array[]::bigint[],to_timestamp(0),array[]::bigint[])'
        #cursor.execute(stmt,param_li)
        #cnx = cursor.connection
        #cnx.commit()
    except Exception as e:
        print(e)
def retrieve_account_id_from_name(name,cursor=None):
    # cursor needs to exist dont do cursor creation
    # retrieve data from server
    # if the account_id exists and matches up, then a-okay no update
    # if account_id exists undera  different name. then update that account_ids name
    # and then recurse this function for that name
    # because its possible that name exists under a
    # modules robust if api down
    print(name)
    retrieved = False
    account_id = account_id_from_name_refresh(name)
    try:
        acc = Account.objects.get(account_id=account_id)
        if name.lower() != acc.name.lower():
            acc.name = name
            acc.save()
    except Account.DoesNotExist as e:
        print(e)
        insert_new_account(account_id,name,cursor)
    return account_id

# account_id_from_name function
# Top Level Function
# gets account id from a name argument
# input : name = summoner name : string
# output : account_id : int/long
def account_id_from_name(name,cursor=None):
    acc_id = retrieve_account_id_from_name(name,cursor)
    return acc_id

# get_acc_id_for_group function
# Top Level Function
# gets list of account ids from a list of names
# input : name_li = list of summoner names = List[string]
# output : account_id : List[int/long]
def get_acc_id_for_group(name_li,cursor=None):
    acc_id_li = []
    for n in name_li:
        acc_id = account_id_from_name(n,cursor)
        if acc_id is not None:
            acc_id_li.append(acc_id)
    return acc_id_li

# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    pass

# cleanup function
# does all necessary tasks at the end of the script to use the module correctly
# and save results from processing
def cleanup():
    pass

#testing function to make sure its all good

def inner_testing():
    print(exists_already('E94Qwk4wKcW0u2H34tZ-qGOOQxX8OnyNTItJUwB6zdDIDg',None))
    print(exists_already('herp',None))

def testing():
    #inner_testing()
    with league_util.conn_postgre() as cnx:
        with cnx.cursor() as cursor:
            a_k = {}
            a_k['chulchultrain'] = 'PhjloNxjxrIOTQ4trcehe8OGiU9ABj933DBGRnO4GBfqNw'
            a_k['chulminyang'] = 'XfVmqID5O2tHwGU0wroo7AM2JGYXSnbouxR4np57zd1NQw'
            a_k['crysteenah'] = 'bvw_nI2IATn8zNJosGoqNacUFUURmWRjMy-mrbWksN75gw'
            a_k['blanket robber'] = 'Apa_1kMg9ckSifHjbmEqdivPV1ZE-PG0VBDsFblbnDfxCA'
            a_k['starcalls coffee'] = 'JwdAIS2YHVF6vbxgHOIbgll7FMsfZIXyQv8k9hhmUl2JEw'
            a_k['ilovememundo'] = 'jIMdQTRS3qiNR2EpHFnKQug9UTN-7N2xgj-UhrY6Cdj9HA'
            a_k['sbaneling'] = 'E6QXRg4OdwKEWvebh8NjjLDTixMf5ncFKhc380Xud9TN2D0'
            a_k['pebblekid'] = 'ag0vyR9w6id7cJhGTkJpu4aEGkK_V5-gZW1QFYcltcVzpRs'
            for x in a_k:
                #assert(a_k[x] == account_id_from_name(x,cursor))
                print(account_id_from_name(x,cursor))
            print(account_id_from_name('summontheez',cursor))


setup()
if __name__ == "__main__":
    #inner_testing()
    testing()
cleanup()
