import league_curl
import league_conf
import pickle
import subprocess
import league_util

#   Will map accounts to the list of match data.
#
#   Instead of refreshing the entire list everytime, which will take up network bandwidith.
#   We keep track of when the last time the matchdata was refreshed for each account we have on hand.
#
#
#
#
#
#
#
#

acc_to_match = {}
acc_refresh_timestamp = {}

# load_acc_to_match_map function
# this function will create/load the map that
# maps account id to match_id list from the data structure file
# indicated by our configuration
def load_acc_to_match_map():
    fin = None
    try:
        fin = open(league_conf.acc_match_file,'rb')
        res = pickle.load(fin)
        fin.close()
    except IOError:
        print("Couldnt load pickled acc match data file")
        res = {}
    finally:
        if fin != None:
            fin.close()
    return res

# save_acc_to_match_map function
# this function will save acc_to_match map
# to the appropriate data structure file indicated by our configuration
def save_acc_to_match_map(acc_to_match):
    with open(league_conf.acc_match_file,'wb') as fout:
        pickle.dump(acc_to_match,fout)

# load_acc_refresh_timestamp_map function
# this function will create/load the map that
# maps account_id to the timestamp that indicates when that account's
# matchlist data was last refreshed.
# from the data structure file indicated by our configuration
def load_acc_refresh_timestamp_map():
    fin = None
    try:
        fin = open(league_conf.acc_refresh_file,'rb')
        res = pickle.load(fin)
        fin.close()
    except IOError:
        print("Couldnt load pickled acc refresh file")
        res = {}
    finally:
        if fin != None:
            fin.close()
        return res

# save_acc_refresh_timestamp_map function
# this function will save acc_refresh_timestamp to the
# appropriate data structure file indicated by our configuration
def save_acc_refresh_timestamp_map(acc_refresh_timestamp):
    with open(league_conf.acc_refresh_file,'wb') as fout:
        pickle.dump(acc_refresh_timestamp,fout)

# matches_refresh function
# low level function
# calls the Riot API to get a list of all the new matches that an
# account has played after the timestamp associated with that account id
# inside our acc_refresh_timestamp map, and updates that map with the
# current timestamp
#TODO: becauase we're not actually updating our acc_to_match map here,
# we should not actually update the timestamp map here because
# it could cause desync. Either do both or neither.
def matches_refresh(id):
    global acc_refresh_timestamp
    if id not in acc_refresh_timestamp:
        last_timestamp = 0
    else:
        last_timestamp = acc_refresh_timestamp[id]
    acc_match_data = league_curl.request('match_list',id,{'beginTime':last_timestamp})
    if acc_match_data is None:
        raise RuntimeError("Couldn't retrieve match data for the account id " + str(id))
    cur_timestamp = league_util.get_current_timestamp()
    acc_refresh_timestamp[id] = cur_timestamp
    return acc_match_data['matches']

#
#
#
#
def new_matches_from_id(id):
    try:
        new_match_data = matches_refresh(id)
    except RuntimeError as e:
        print(e)
        new_match_data = None
    if new_match_data is not None:
        acc_to_match[id] = new_match_data + acc_to_match[id]
    return new_match_data

#
#   Just returns the list of match_data
#   Refreshes everytime and updates the account refresh timestamp to the current timestamp
#
def matches_from_id(id):
    try:
        new_match_data = matches_refresh(id)
    except RuntimeError as e:
        print(e)
        new_match_data = None
    if new_match_data is None:
        if id in acc_to_match:
            return acc_to_match[id]
        else:
            return None
    else:
        if id not in acc_to_match:
            acc_to_match[id] = []
        acc_to_match[id] = new_match_data + acc_to_match[id]
        return acc_to_match[id]

# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    global acc_to_match
    global acc_refresh_timestamp
    acc_to_match = load_acc_to_match_map()
    acc_refresh_timestamp = load_acc_refresh_timestamp_map()

# cleanup function
# does all necessary tasks at the end of the script to use the module correctly
# and save results from processing
# Note: Should really be called at the end of the caller scripts life.
def cleanup():
    global acc_to_match
    global acc_refresh_timestamp
    save_acc_to_match_map(acc_to_match)
    save_acc_refresh_timestamp_map(acc_refresh_timestamp)

def testing():
    pass
setup()
#testing()
cleanup()
