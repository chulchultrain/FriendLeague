import league_curl
import league_conf
import pickle
import subprocess

name_to_account_data = {}

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

def save_name_to_account_map(name_to_account):
    fout = open(league_conf.name_acc_file,'wb')
    pickle.dump(name_to_account,fout)
    fout.close()

#TODO: What should happen when 4XX error?
def account_data_from_name_refresh(name):
    account_data = league_curl.request('summoner',name)
    if account_data is None:
        raise RuntimeError("Couldn't retrieve data for the summoner name " + name)
    return account_data

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



def account_id_from_name(name):
    acc_data = account_data_from_name(name)
    if acc_data is None:
        return None
    else:
        return acc_data['accountId']

def setup():
    global name_to_account_data
    name_to_account_data = load_name_to_account_map()

def cleanup():
    global name_to_account_data
    save_name_to_account_map(name_to_account_data)

def testing():
    print(account_id_from_name('chulchultrain'))
    print(account_id_from_name('crysteenah'))
    print(account_id_from_name('gosusummoner'))
    print(account_id_from_name('timbangu'))
    print(account_id_from_name('summontheez'))
    print(account_id_from_name('timban'))

setup()
testing()
cleanup()
