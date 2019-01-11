import leagreq.league_curl as league_curl
import utils.league_util as league_util
import utils.filemap as filemap
import utils.tinydbmap as tinydbmap
import utils.sqlitemap as sqlitemap
import league_conf
import pickle
import psycopg2
import json

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

#
#   try to retrieve match data from our database
#   return None is does not exist
#
def retrieve_match_data(match_id,cursor):
    stmt = 'select match_data from analytics_match_detail where match_id = %s'
    cursor.execute(stmt,[match_id])
    try:
        match_data = cursor.fetchone()
        if match_data is not None:
            match_data = match_data[0]
    except psycopg2.ProgrammingError:
        match_data = None
    return match_data

def insert_match_data(match_id,match_data,cursor):
    #TODO:
    match_data_str = json.dumps(match_data)
    stmt = 'insert into analytics_match_detail values(%s,%s)'
    cursor.execute(stmt,[match_id,match_data_str])
    cnx = cursor.connection()
    cnx.commit()


# match_data_from_id function
# high level function
# this function returns the desired match data given a match id.
def match_data_from_id(match_id,cursor):
    match_data = retrieve_match_data(match_id,cursor)
    if match_data is None:
        match_data = match_data_refresh(match_id)
        if match_data is None:
            print("Could not find data for match {0}".format(match_id))
        else:
            insert_match_data(match_id,match_data,cursor)
    return match_data

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
def map_account_id_to_participant_id(m_d):
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

def map_acc_id_to_participant_data(match_data,acc_id_li):
    res = {}
    for a in acc_id_li:
        pd = player_data_from_match(match_data,a)
        if pd is not None:
            res[a] = pd
    return res

def team_data(match_data,part_id):
    p_data = find_participant_data(match_data,part_id)
    team_id = p_data['teamId']
    for t in match_data['teams']:
        if t['teamId'] == team_id:
            return t
    return None

def map_team_id_to_part_ids(match_data):
    res = {}
    for t in match_data['teams']:
        cur_team_id = t['teamId']
        res[cur_team_id] = []
    for p in match_data['participants']:
        t_id = p['teamId']
        res[t_id].append(p['participantId'])
    return res

def find_team_from_id_li(m_d,acc_id_li):
    for a in acc_id_li:
        p_id = find_part_id(m_d,a)
        if p_id is not None:
            t_id = find_participant_data(m_d,p_id)['teamId']
            return t_id
    return None

def find_other_team_from_id_li(m_d,acc_id_li):
    t_id = find_team_from_id_li(m_d,acc_id_li)
    teams = m_d['teams']
    for t in teams:
        if t['teamId'] is not t_id:
            return t['teamId']
    return None
# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    pass

def calc_cs(pd):
    stats = pd['stats']
    return stats['totalMinionsKilled'] + stats['neutralMinionsKilled']

def transform_lane(rough_lane):
    if rough_lane == u'MID':
        rough_lane = u'MIDDLE'
    if rough_lane == u'BOT':
        rough_lane = u'BOTTOM'
    return rough_lane
def map_pid_role(m_d):
    p_li = m_d['participants']
    res = {}
    tid_to_bot_li = {}
    for p in p_li:
        pid = p['participantId']
        tid = p['teamId']
        rough_lane = p['timeline']['lane']
        rough_lane = transform_lane(rough_lane)
        if rough_lane == u'BOTTOM':
            if tid not in tid_to_bot_li:
                tid_to_bot_li[tid] = []
            tid_to_bot_li[tid].append([pid,p])
        res[pid] = rough_lane
    for t in tid_to_bot_li:
        entry = tid_to_bot_li[t]
        if len(entry) == 2:
            one = entry[0]
            two = entry[1]
            if calc_cs(one[1]) > calc_cs(two[1]): #one is AD other is support.
                res[two[0]] = u'SUPPORT'
            else:
                res[one[0]] = u'SUPPORT'
    return res

def calc_role(p_d):
    timeline = p_d['timeline']
    rough_lane = timeline['lane']
    role = timeline['role']
    if rough_lane == u'MID':
        rough_lane = u'MIDDLE'
    if rough_lane == u'BOT':
        rough_lane = u'BOTTOM'
    if role == 'DUO_SUPPORT':
        rough_lane = 'SUPPORT'
    return rough_lane

def inter_map(m_d):
    res = {}
    pi_li = m_d['participantIdentities']
    p_li = m_d['participants']
    t_li = m_d['teams']
    team_id_part_ids = {}
    team_id_part_data = {}
    team_id_team_data = {}
    p_id_role = {}
    #TODO: ROLE MAPPING TODO TODO
    for p in p_li:
        tid = p['teamId']
        pid = p['participantId']
        if tid not in team_id_part_ids:
            team_id_part_ids[tid] = []
        if tid not in team_id_part_data:
            team_id_part_data[tid] = []
        team_id_part_ids[tid].append(pid)
        team_id_part_data[tid].append(p)
    for t in t_li:
        team_id_team_data[t['teamId']] = t
    for pi in pi_li:
        acc_id = pi['player']['accountId']
        p_id = pi['participantId']
        t_id = None
        for p in p_li:
            if p['participantId'] == p_id:
                t_id = p['teamId']
                pd = p
                break
        role = calc_role(pd)
        res[(acc_id,p_id,t_id,calc_role(pd))] = {'pd':pd,'td':team_id_team_data[t_id],'pot':team_id_part_ids[t_id],'tpd':team_id_part_data[t_id]}
    return res
#id_type : "account id, participant id, team id "
#result_type : "account id, participant id, team id, participant data, team data, participants on team data"

def convert_type_to_index(input_type):
    if input_type == 'account_id':
        res = 0
    elif input_type == 'participant_id':
        res = 1
    elif input_type == 'team_id':
        res = 2
    elif input_type == 'role':
        res = 3
    elif input_type == 'part_data':
        res = 'pd'
    elif input_type == 'team_data':
        res = 'td'
    elif input_type == 'parts_on_team':
        res = 'pot'
    elif input_type == 'team_part_data':
        res = 'tpd'
    else:
        res = None
    return res
def id_to_data(in_map,id,id_type="account_id",result_type="participant_id"):
    id_index = convert_type_to_index(id_type)
    #print(id_index)
    result_index = convert_type_to_index(result_type)
    #print(result_index)
    res = None
    for p in in_map:
        #print(p)
        if p[id_index] == id:
            if type(result_index) is int:
                res = p[result_index]
            else:
                res = in_map[p][result_index]
            break
    return res

def enemy_team_id(in_map,team_id):
    t_id_ind = convert_type_to_index('team_id')
    if type(t_id_ind) is not int:
        print("Problem with connvert_type_to_ind")
        return None
    for p in in_map:
        if type(t_id_ind) is int:
            if p[t_id_ind] is not team_id:
                return p[t_id_ind]
    return None
# participant id
# participant data
# team id from id li
# team data from team id
# team data from participant_id
# participant data from players on a team
#
# this module really should only have basic functionality on getting data, so really
# only getting teams and getting participants
#



#
# cleanup function
# does all necessary tasks at the end of the script to use the module correctly
# and save results from processing
# Note: Should really be called at the end of the caller scripts life.
def cleanup():
    pass

def testing():
    with league_util.conn_postgre() as cnx:
        with cnx.cursor() as cursor:
            r = match_data_from_id(2859270267,cursor)
            #print(r)
            m = inter_map(r)
            for x in m:
                print(x)
            mm = id_to_data(m,239590109,id_type='account_id',result_type='participant_id')
            rr = id_to_data(m,7,id_type='participant_id',result_type='account_id')
            ww = id_to_data(m,7,id_type='participant_id',result_type='team_id')
            ee = id_to_data(m,7,id_type='participant_id',result_type='parts_on_team')
            dd = id_to_data(m,200,id_type='team_id',result_type='team_data')
            aa = id_to_data(m,7,id_type='participant_id',result_type='team_data')
            asdf = id_to_data(m,7,id_type='participant_id',result_type='role')
            pd = id_to_data(m,7,id_type='participant_id',result_type='part_data')
            print(mm)
            print(rr)
            print(ww)
            print(ee)
            print(aa)
            print(dd)
            print(asdf)
            print(pd['timeline'])
            #print(r['gameMode'])
            #print(r['gameType'])
            #print(r['gameVersion'])
            #print(players_from_match(2526402692))
            #print(match_data_from_id(2524795289))
            #print(get_match_win(2524795289,32421132))
        cnx.commit()


setup()
if __name__ == '__main__':
    testing()
cleanup()
