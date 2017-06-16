import league_curl
import league_util
import league_conf
import pickle

match_id_to_data = {}

def load_match_data_map():
    fin = None
    try:
        fin = open(league_conf.match_data_file,'rb')
        res = pickle.load(fin)
        fin.close()
    except IOError:
        print("Couldnt load pickled match data file")
        res = {}
    except EOFError:
        print("Couldnt load pickled match data file")
        res = {}
    finally:
        if fin != None:
            fin.close()
    return res

def save_match_data_map(acc_to_match):
    with open(league_conf.match_data_file,'wb') as fout:
        pickle.dump(acc_to_match,fout)

def match_data_refresh(match_id):
    match_data = league_curl.request('match',match_id)
    if match_id is None:
        return None
    return match_data

def match_data_from_id(match_id):
    if match_id not in match_id_to_data:
        match_data = match_data_refresh(match_id)
        if match_data != None:
            match_id_to_data[match_id] = match_data
        return match_data
    else:
        return match_id_to_data[match_id]

def players_from_match(match_id):
    pass #TODO:IMPLEMENT
def setup():
    global match_id_to_data
    match_id_to_data = load_match_data_map()

def cleanup():
    global match_id_to_data
    save_match_data_map(match_id_to_data)

def testing():
    print(match_data_from_id(2524795289))


setup()
testing()
cleanup()
