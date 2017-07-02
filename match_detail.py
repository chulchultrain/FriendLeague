import league_curl
import league_util
import league_conf
import pickle

match_id_to_data = {}

# load_match_data_map function
# this function will create/load the map that
# maps match_id to match_data from the data structure file
# indicated by our configuration
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

# save_match_data_map function
# this function will save our match_id to match_data map
# to the appropriate data structure file indicated by our configuration
def save_match_data_map(acc_to_match):
    with open(league_conf.match_data_file,'wb') as fout:
        pickle.dump(acc_to_match,fout)

# match_data_refresh function
# low level function
# makes a request to the Riot API for the desired match data
# given the match id.
def match_data_refresh(match_id):
    match_data = league_curl.request('match',match_id)
    if match_id is None:
        return None
    return match_data

# filter_match_data_for_storage function
# low level function
# takes just the desired properties of match data given the full match data.
# in order to save disk space
# and not have problems loading the entire match data map into memory
# whenever load_match_data_map is called.
def filter_match_data_for_storage(match_data):
    res = {}
    for x in match_data:
        res[x] = match_data[x]
    participant_data = res['participants']
    keep_fields = ['participantId','teamId']

    for p in participant_data:
        p_keys = p.keys()
        for x in p_keys:
            if x not in keep_fields:
                p.pop(x)

    team_data = match_data['teams']
    keep_fields = ['teamId','win']
    for t in team_data:
        t_keys = t.keys()
        for x in t_keys:
            if x not in keep_fields:
                t.pop(x)

    keep_fields = ['accountId','summonerName']
    p_i_d = res['participantIdentities']
    for p in p_i_d:
        player = p['player']
        p_keys = player.keys()
        for x in p_keys:
            if x not in keep_fields:
                player.pop(x)
    return res
    pass #TODO

# match_data_from_id function
# high level function
# this function returns the desired match data given a match id.
def match_data_from_id(match_id):
    if match_id not in match_id_to_data:
        match_data = match_data_refresh(match_id)
        if match_data != None:
            match_data = filter_match_data_for_storage(match_data)
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
    r = match_data_from_id(3103315446)
    print(r)
    #print(r['gameMode'])
    #print(r['gameType'])
    #print(r['gameVersion'])
    #print(players_from_match(2526402692))
    #print(match_data_from_id(2524795289))
    #print(get_match_win(2524795289,32421132))


setup()
#testing()
cleanup()
