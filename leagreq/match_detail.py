import leagreq.league_curl as league_curl
import utils.league_util as league_util
import utils.filemap as filemap
import utils.tinydbmap as tinydbmap
import utils.sqlitemap as sqlitemap
import league_conf
import pickle

match_id_to_data = {}

# load_match_data_map function
# this function will create/load the map that
# maps match_id to match_data from the data structure file
# indicated by our configuration
def load_match_data_map():
    #res = league_util.load_pickled_map(league_conf.match_data_file)
    #res = filemap.Filemap(league_conf.match_data_dir)
    #res = tinydbmap.TinyDBMap(league_conf.match_data_db,'gameId')
    res = sqlitemap.SqliteMap(league_conf.match_data_db)
    return res
# save_match_data_map function
# this function will save our match_id to match_data map
# to the appropriate data structure file indicated by our configuration
def save_match_data_map(acc_to_match):
    #league_util.save_pickled_map(league_conf.match_data_file,acc_to_match)
    pass

# match_data_refresh function
# low level function
# makes a request to the Riot API for the desired match data
# given the match id.
def match_data_refresh(match_id):
    match_data = league_curl.request('match',match_id)
    if match_id is None:
        print("COULDNT FIND MATCH " + str(match_id))
        return None
    return match_data



# match_data_from_id function
# high level function
# this function returns the desired match data given a match id.
def match_data_from_id(match_id):
    if match_id not in match_id_to_data:
        match_data = match_data_refresh(match_id)
        if match_data != None:
            #match_data = filter_match_data_for_storage(match_data)
            match_id_to_data[match_id] = match_data
        return match_data
    else:
        return match_id_to_data[match_id]

# players_from_match function
# high level function
# this function returns the list of account_ids of players
# that are present in a match given the match id.
def players_from_match(match_id):
    m_d = match_data_from_id(match_id)
    if m_d == None:
        return None

    participant_identities_data = m_d['participantIdentities']
    res = []
    for p in participant_identities_data:
        res.append(p['player']['accountId'])
    return res
# DEPRECATED
def map_account_id_to_participant_id(match_id):
    m_d = match_data_from_id(match_id)
    if m_d == None:
        return None
    res = {}
    part_list = m_d['participantIdentities']
    for x in part_list:
        res[x['player']['accountId']] = x['participantId']
    return res

#match detailed obj, id = int
def find_part_id(match,id):
    part_id_li = match['participantIdentities']
    for p in part_id_li:
        if p['player']['accountId'] == id:
            return p['participantId']
    return None

def find_participant_data(match,part_id):
    parts = match['participants']
    for p in parts:
        if p['participantId'] == part_id:
            return p
    return None

def player_data_from_match(match_data,acc_id):
    part_id = find_part_id(match_data,acc_id)
    res = find_participant_data(match_data,part_id)
    return res


def team_data(match_data,part_id):
    p_data = find_participant_data(match_data,part_id)
    team_id = p_data['teamId']
    for t in match_data['teams']:
        if t['teamId'] == team_id:
            return t
    return None

# DEPRECATED
def map_participant_id_to_participant_data(match_id):
    m_d = match_data_from_id(match_id)
    if m_d == None:
        return None
    res = {}
    part_list = m_d['participants']
    for p in part_list:
        res[p['participantId']] = p
        print(p['teamId'])
    return res

#TODO: REDO Because Removed participants stats from data
# DEPRECATED
def get_match_win(match_id,account_id):
    acc_to_part = map_account_id_to_participant_id(match_id)
    if account_id not in acc_to_part:
        return None
    participant_data_map = map_participant_id_to_participant_data(match_id)
    res = participant_data_map[acc_to_part[account_id]]['stats']['win']
    return res



# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    global match_id_to_data
    match_id_to_data = load_match_data_map()

# cleanup function
# does all necessary tasks at the end of the script to use the module correctly
# and save results from processing
# Note: Should really be called at the end of the caller scripts life.
def cleanup():
    global match_id_to_data
    save_match_data_map(match_id_to_data)

def testing():
    r = match_data_from_id(2859270267)
    print(r)
    #print(r['gameMode'])
    #print(r['gameType'])
    #print(r['gameVersion'])
    #print(players_from_match(2526402692))
    #print(match_data_from_id(2524795289))
    #print(get_match_win(2524795289,32421132))


setup()
if __name__ == '__main__':
    testing()
cleanup()
