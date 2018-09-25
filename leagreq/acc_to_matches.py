import leagreq.league_curl as league_curl
import league_conf
import pickle
import subprocess
import utils.league_util as league_util
import utils.filemap as filemap
import sets

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
    #res = league_util.load_pickled_map(league_conf.acc_match_file)
    res = filemap.Filemap(league_conf.acc_match_dir)
    return res

# save_acc_to_match_map function
# this function will save acc_to_match map
# to the appropriate data structure file indicated by our configuration
def save_acc_to_match_map(acc_to_match):
    #league_util.save_pickled_map(league_conf.acc_match_file,acc_to_match)
    pass
# load_acc_refresh_timestamp_map function
# this function will create/load the map that
# maps account_id to the timestamp that indicates when that account's
# matchlist data was last refreshed.
# from the data structure file indicated by our configuration
def load_acc_refresh_timestamp_map():
    #res = league_util.load_pickled_map(league_conf.acc_refresh_file)
    res = filemap.Filemap(league_conf.acc_timestamp_dir)
    return res

# save_acc_refresh_timestamp_map function
# this function will save acc_refresh_timestamp to the
# appropriate data structure file indicated by our configuration
def save_acc_refresh_timestamp_map(acc_refresh_timestamp_map):
    #league_util.save_pickled_map(league_conf.acc_refresh_file,acc_refresh_timestamp_map)
    pass
# matches_refresh function
# low level function
# calls the Riot API to get a list of all the new matches that an
# account has played after the timestamp associated with that account id
# inside our acc_refresh_timestamp map

def request_remaining_games(id,beginTime):
    cur_match = 0
    cur_season = 11
    param_map = {'beginTime':beginTime,'beginIndex':cur_match}
    param_map['seasonId'] = 11
    acc_match_data = league_curl.request('match_list',id,param_map)
    matches = []
    while(acc_match_data is not None and cur_match  < acc_match_data['totalGames']):
        matches += acc_match_data['matches']
        cur_match += 100
        param_map['beginIndex'] = cur_match
        acc_match_data = league_curl.request('match_list',id,param_map)
    return matches

def matches_refresh(id):
    global acc_refresh_timestamp
    res_match_data = []
    if id not in acc_refresh_timestamp:
        last_timestamp = 0
    else:
        last_timestamp = acc_refresh_timestamp[id]
    new_matches = request_remaining_games(id,last_timestamp)
    total_games = new_matches
    if total_games is None:
        raise RuntimeError("Couldn't retrieve match data for the account id " + str(id))
    cur_timestamp = league_util.get_current_timestamp()

    return cur_timestamp,total_games

# update_match_data function
# low level function
# simply updates the acc_to_match map at id key with new_match_data values
def update_match_data(id,new_match_data):
    global acc_to_match
    if id not in acc_to_match:
        acc_to_match[id] = []
    acc_to_match[id] = new_match_data + acc_to_match[id]

# update_acc_refresh function
# low level function
# simply updates the acc_refresh_timestamp map at id key with new_timestamp value
def update_acc_refresh(id,new_timestamp):
    global acc_refresh_timestamp
    if id not in acc_refresh_timestamp:
        acc_refresh_timestamp[id] = 0
    acc_refresh_timestamp[id] = new_timestamp

# new_matches_from_id function
# high level function
# loads a list of the new matches acssociated with an account.
# new being the matches after the timestamp associated with that account id
# inside the acc_refresh_timestamp map
def new_matches_from_id(id):
    global acc_refresh_timestamp
    global acc_to_match
    try:
        cur_timestamp,new_match_data = matches_refresh(id)
    except RuntimeError as e:
        print(e)
        new_match_data = None
    if new_match_data is not None:
        if(id not in acc_to_match):
            acc_to_match[id] = []
        acc_to_match[id] = new_match_data + acc_to_match[id]
        acc_refresh_timestamp[id] = cur_timestamp
    return new_match_data

# matches_from_id function
# high level function
# returns the list of matches associated with an account id
def matches_from_id(id):
    global acc_to_match
    try:
        cur_timestamp,new_match_data = matches_refresh(id)
    except RuntimeError as e:
        print(e)
        new_match_data = None
    if new_match_data is not None:
        update_match_data(id,new_match_data)
        update_acc_refresh(id,cur_timestamp)
    if id in acc_to_match:
        return acc_to_match[id]
    else:
        return None

def is_solo_match(match):
    return match['queue'] == 420

def is_flex_match(match):
    return match['queue'] == 440

#high-level function
#gets all solo queue matches for a given id
#by filtering on all the matches for the solo queue type
def solo_q_matches(id):
    total_matches = matches_from_id(id)
    res = []
    for x in total_matches:
        if is_solo_match(x):
            res.append(x)
    return res

#high-level function
#gets all solo queue matches for a given id
#by filtering on all the matches for the flex queue type
def flex_q_matches(id):
    total_matches = matches_from_id(id)
    res = []
    for x in total_matches:
        if is_flex_match(x):
            res.append(x)
    return res
#
#def filter_matches(id,filter_function):#
    #total_matches = matches_from_id(id)
    #res = p[
    #for x in total_matches:
#        if()
#    ]
def get_flex_match_list_for_group(acc_id_li):
    init_filter = []
    id_set = sets.Set()
    for a in acc_id_li:
        m_li = flex_q_matches(a)
        for m in m_li:
            if m['gameId'] not in id_set:
                if m['gameId'] == 3103315446:
                    print("HERP WAS HERE")
                    print(a)
                init_filter.append(m)
                id_set.add(m['gameId'])
    res = []
    return init_filter

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

#get matches with filter.
#get matches for list with filter
#with flag to refresh 

def testing():
    #print(new_matches_from_id(44649467))
    #print(matches_from_id(44649467))
    print(len(solo_q_matches(38566957)))

setup()
if __name__ == "__main__":
    testing()
cleanup()
