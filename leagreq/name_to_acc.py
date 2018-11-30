import leagreq.league_curl as league_curl
import league_conf
import utils.league_util as league_util
import utils.filemap as filemap
import pickle
import subprocess

name_to_account_data = {}


# load_name_to_account_map function
# this function will create the map
# that maps summoner name to their account data
# by loading all the data we have from the data structure file indicated by
# our configuration.
def load_name_to_account_map():
    return filemap.Filemap(league_conf.name_acc_dir)
    #return league_util.load_pickled_map(league_conf.name_acc_file)


# save_name_to_account_map function
# this function will save the map
# to the proper data structure file indicated by our configuration.
def save_name_to_account_map(name_to_account):
    #league_util.save_pickled_map(league_conf.name_acc_file,name_to_account)
    pass
#TODO: What should happen when 4XX error?
# account_data_from_name_refresh function
# low level function
# makes an explicit request to the Riot API for the desired account data
# given a summoner name
def account_data_from_name_refresh(name):
    account_data = league_curl.request('summoner',name)
    if account_data is None:
        raise RuntimeError("Couldn't retrieve data for the summoner name " + name)
    return account_data

# account_data_from_name function
# Top Level function
# gets account data from a name argument
# input : name : summoner name : string
# output : account data : summonerDTO type from Riot API
def account_data_from_name(name):
    global name_to_account_data
    if name not in name_to_account_data:
        try:
            print("COULDNT FIND IN MAP " + name)
            name_to_account_data[name] = account_data_from_name_refresh(name)
            return name_to_account_data[name]
        except RuntimeError as e:
            print(e)
            return None
    else:
        return name_to_account_data[name]


# account_id_from_name function
# Top Level Function
# gets account id from a name argument
# input : name = summoner name : string
# output : account_id : int/long
def account_id_from_name(name):
    acc_data = account_data_from_name(name)
    if acc_data is None:
        return None
    else:
        return acc_data['accountId']

# get_acc_id_for_group function
# Top Level Function
# gets list of account ids from a list of names
# input : name_li = list of summoner names = List[string]
# output : account_id : List[int/long]
def get_acc_id_for_group(name_li):
    acc_id_li = []
    for n in name_li:
        acc_id = account_id_from_name(n)
        if acc_id is not None:
            acc_id_li.append(acc_id)
    return acc_id_li

# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    global name_to_account_data
    name_to_account_data = load_name_to_account_map()

# cleanup function
# does all necessary tasks at the end of the script to use the module correctly
# and save results from processing
def cleanup():
    global name_to_account_data
    save_name_to_account_map(name_to_account_data)

#testing function to make sure its all good
def testing():
    a_k = {}
    a_k['chulchultrain'] = 44649467
    a_k['chulminyang'] = 38566957
    a_k['crysteenah'] = 48258111
    a_k['timbangu'] = 32139475
    a_k['starcalls coffee'] = 47916976
    a_k['ilovememundo'] = 33226921
    a_k['sbaneling'] = 230550059
    a_k['1000pingftw'] = 41057569
    a_k['bigheartjohnny'] = 41912122
    a_k['inting griefer'] = 201989747
    a_k['thegoldenpenis'] = 36255338
    for x in a_k:
        assert(a_k[x] == account_id_from_name(x))

setup()
if __name__ == "__main__":
    testing()
cleanup()