import league_curl
import league_conf
import pickle
import subprocess

name_to_account_data = {}


# load_name_to_account_map function
# this function will create the map
# that maps summoner name to their account data
# by loading all the data we have from the data structure file indicated by
# our configuration.
def load_name_to_account_map():
    fin = None
    try:
        fin = open(league_conf.name_acc_file,'rb')
        res = pickle.load(fin)
        fin.close()
    except IOError:
        print("Couldnt load pickled name acc data file")
        return {}
    finally:
        if fin != None:
            fin.close()
    return res


# save_name_to_account_map function
# this function will save the map
# to the proper data structure file indicated by our configuration.
def save_name_to_account_map(name_to_account):
    fout = open(league_conf.name_acc_file,'wb')
    pickle.dump(name_to_account,fout)
    fout.close()

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
# gets account data from a name argument
# high level function
#

def account_data_from_name(name):
    global name_to_account_data
    if name not in name_to_account_data:
        try:
            name_to_account_data[name] = account_data_from_name_refresh(name)
            return name_to_account_data[name]
        except RuntimeError as e:
            print(e)
            return None
    else:
        return name_to_account_data[name]


# account_id_from_name function
# top level function
# gets account id from a name argument
#
def account_id_from_name(name):
    acc_data = account_data_from_name(name)
    if acc_data is None:
        return None
    else:
        return acc_data['accountId']

# setup function
# does all necessary tasks to use this entire module correctly
#
def setup():
    global name_to_account_data
    name_to_account_data = load_name_to_account_map()

# cleanup function
# does all necessary tasks at the end of the script to use the module correctly
# and save results from processing
# Note: Should really be called at the end of the caller scripts life.
def cleanup():
    global name_to_account_data
    save_name_to_account_map(name_to_account_data)


def testing():
    print('chulchultrain ' + str(account_id_from_name('chulchultrain')))
    print('crysteenah ' + str(account_id_from_name('crysteenah')))
    print('gosusummoner ' + str(account_id_from_name('gosusummoner')))
    print('timbangu ' + str(account_id_from_name('timbangu')))
    print('summontheez ' + str(account_id_from_name('summontheez')))
    print('king doran' + str(account_id_from_name('king doran')))
    print('krazen ' + str(account_id_from_name('krazen')))
    print('black zealot ' + str(account_id_from_name('black zealot')))
    print('chulminyang ' + str(account_id_from_name('chulminyang')))
    print('starcalls coffee ' + str(account_id_from_name('starcalls coffee')))
    print('mikiilolirl ' + str(account_id_from_name('mikiilolirl')))
    print('fearbreeder ' + str(account_id_from_name('fearbreeder')))
    print('tsm taha ' + str(account_id_from_name('tsm taha')))
    print('datevape ' + str(account_id_from_name('datevape')))

setup()
testing()
cleanup()
