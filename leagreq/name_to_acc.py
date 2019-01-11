import leagreq.league_curl as league_curl
import league_conf
import utils.league_util as league_util
import utils.filemap as filemap
import pickle
import subprocess

name_to_account_data = {}



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
    cursor.execute('select account_id from analytics_account where id=%s',account_id)
    try:
        s = cursor.fetchone()
        return s is not None
    except:
        return False

def insert_new_account(account_id,name,cursor):
    big_int_array = 'array[]::bigint[]'
    to_timestamp_0 = 'to_timestamp(0)'
    param_li = [account_id,name]
    try:
        cursor.execute('insert into analytics_account values(%s,%s,array[]::bigint[],to_timestamp(0),array[]::bigint[])',param_li)
        cnx = cursor.connection
        cnx.commit()
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
    cursor.execute('select name from analytics_account where account_id = %s',[account_id])
    seen_account_name = None
    #cursor.execute('select account_id from analytics_account where name = %s',[name])
    try:
        row = cursor.fetchone()
        if row is not None:
            seen_account_name = row[0]
    except:
        seen_account_name = None
        pass
    print(account_id)
    if seen_account_name is None:
        insert_new_account(account_id,name,cursor)
    elif seen_account_name is not name:
        try:
            cursor.execute('update analytics_account set name=%s where account_id =%s',[name,account_id])
            cnx = cursor.connection
            cnx.commit()
        except Exception as e:
            print(e)
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
def testing():
    with league_util.conn_postgre() as cnx:
        with cnx.cursor() as cursor:
            a_k = {}
            a_k['chulchultrain'] = 'E94Qwk4wKcW0u2H34tZ-qGOOQxX8OnyNTItJUwB6zdDIDg'
            a_k['chulminyang'] = 'YHZxJ6M8JP_0Ck88iwgwvrC0Edub3vRUBzMv6vR4CF293w'
            a_k['crysteenah'] = 'iCu9bp2VLrsnq1cUMqDeE3R1rSgEbZnu99BXT07CpmBx3Q'
            a_k['blanket robber'] = 'u4j74jeLLZgQoUwjkMxsOuukHunraQpv7LtFuft99cx0Ow'
            a_k['starcalls coffee'] = '5ukTT5PUJI-1exEIGIGz2zNoS2d5nWfgtgHdN7eipmIUZg'
            a_k['ilovememundo'] = 'CS9Na6UJ3cMwUHV13CGgjsddXiXlZ_P2DaeODZgf4LDQuw'
            a_k['sbaneling'] = '5JZCl447vMc_ym7ScniqYQMO7-zT3J-PAKenjvH7vuGGifM'
            a_k['pebblekid'] = 'CE_LjdDWMle7WDawaEerNpnt2kU2wqEFSVKG8WE3HGtNJbo'
            for x in a_k:
                assert(a_k[x] == account_id_from_name(x,cursor))
                #print(account_id_from_name(x,cursor))
            print(account_id_from_name('summontheez',cursor))


setup()
if __name__ == "__main__":
    testing()
cleanup()
