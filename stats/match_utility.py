import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'FriendLeague.settings'
import django
from django.conf import settings
if __name__ == '__main__':
    django.setup()
import leagreq.match as match

# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    pass

def calc_cs(pd):
    stats = pd['stats']
    return stats['totalMinionsKilled'] + stats['neutralMinionsKilled']

# def transform_lane(rough_lane):
#     if rough_lane == u'MID':
#         rough_lane = u'MIDDLE'
#     if rough_lane == u'BOT':
#         rough_lane = u'BOTTOM'
#     return rough_lane
# def map_pid_role(m_d):
#     p_li = m_d['participants']
#     res = {}
#     tid_to_bot_li = {}
#     for p in p_li:
#         pid = p['participantId']
#         tid = p['teamId']
#         rough_lane = p['timeline']['lane']
#         rough_lane = transform_lane(rough_lane)
#         if rough_lane == u'BOTTOM':
#             if tid not in tid_to_bot_li:
#                 tid_to_bot_li[tid] = []
#             tid_to_bot_li[tid].append([pid,p])
#         res[pid] = rough_lane
#     for t in tid_to_bot_li:
#         entry = tid_to_bot_li[t]
#         if len(entry) == 2:
#             one = entry[0]
#             two = entry[1]
#             if calc_cs(one[1]) > calc_cs(two[1]): #one is AD other is support.
#                 res[two[0]] = u'SUPPORT'
#             else:
#                 res[one[0]] = u'SUPPORT'
#     return res

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
        res[(acc_id,p_id,t_id,role)] = {'pd':pd,'td':team_id_team_data[t_id],'pot':team_id_part_ids[t_id],'tpd':team_id_part_data[t_id]}
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

def id_type_to_li(in_map,id_type="account_id"):
    id_index = convert_type_to_index(id_type)
    if type(id_index) is not int:
        return None
    res = []
    for p in in_map:
        if p[id_index] not in res:
            res.append(p[id_index])
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

def testing():
    r = match.match_data_from_id(2859270267)
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
    print(id_type_to_li(m,id_type='account_id'))
    print(id_type_to_li(m,id_type='team_id'))
    print(id_type_to_li(m,id_type='role'))

def cleanup():
    pass

testing()
