import leagreq.match_detail as match_detail
import leagreq.name_to_acc as name_to_acc
import leagreq.acc_to_matches as acc_to_matches
import leagreq.champ_detail as champ_detail
import preds.teampreds as teampreds
import preds.gamepreds as gamepreds
import preds.playerpreds as playerpreds
import decimal
import sys
import copy
#
#given a set of matches for an id, calculate performance statistics for that player on that set of games
#i want cs diff against other laner.

#TODO: PROBLEM WITH AGGREGATING TIMELINE IS THAT NOT ALL GAMES
# HAVE THE SAME
def aggregate_timeline():
    pass
# custom aggregation
# what i want is to be able to choose w/e stats i want
# how can i choose the custom stats because its a map, should i keep a map
# of things to be added?
#

def map_default_val(m,val):
    for x in m:
        if isinstance(m[x],dict):
            set_val(m[x],val)
        else:
            m[x] = val

def aggregate_match_in(stats_so_far,count_copy,m):
    pass
def stat_aggregate(m_l,data_points,required_data_func):
    count_copy = copy.deep_copy(data_points)
    map_default_val(count_copy,0)
    stats_so_far = copy.deep_copy(count_copy)
    for m in m_l:
        agg_stat = required_data_func(m)
        aggregate_match_in(stats_so_far,count_copy,agg_stat)
    res = post_agg(stats_so_far,count_copy)
    return res
# cond_to_cond function
# Top-level function
# for a list of matches, find the proportion of matches
# that satisfy success_pred given condition_pred
# input : match_list : list of matches to run the condition predicates
#       : condition_pred : a predicate function that tests for a condition on a match
#       : success_pred : a predicate function that tests for a condition on a match
# output : proportion of games that satisfy the success_predicate
# given that the condition predicate was true
def cond_to_cond(match_list,condition_pred,success_pred):
    success,failure = 0,0
    for m in match_list:
        #print(m)
        if condition_pred(m):
            if success_pred(m):
                success += 1
            else:
                failure += 1
    total = success + failure
    print("TOTAL: " + str(total))
    print("SUCCESS: " + str(success))
    print("FAILURE: " + str(failure))
    return success * 1.0 / total * 1.0

#   single_player_stats_wanted function - low-level
#   This just retrieves certain aspects we want from a participant's data
#   and stores them into a map
#   Input: part_data : participant data
#   Output: a map containing only the data we want
#   2018-11-07 : contains cs,wards placed, wards killed, kda,
#   creepsPerMinDeltas 0-10, csDiffPerMinDeltas 0-10
#
def single_player_stats_wanted(part_data):
    res = {}
    p_d = part_data['stats']
    p_t = part_data['timeline']
    res['cs'] = p_d['totalMinionsKilled'] + p_d['neutralMinionsKilled']
    res['wards_placed'] = p_d['wardsPlaced']
    res['wards_killed'] = p_d['wardsKilled']
    res['kills'] = p_d['kills']
    res['deaths'] = p_d['deaths']
    res['damage'] = p_d['totalDamageDealtToChampions']
    res['assists'] = p_d['assists']
    try:
        res['cs10'] = p_t['creepsPerMinDeltas']['0-10']
    except KeyError as e:
        #for k in p_t:
        #    print(k)
        #print("DERP")
        pass
        #sys.exit(-1)
    try:
        res['csdif10'] = p_t['csDiffPerMinDeltas']['0-10']
    except KeyError as e:
        #for k in p_t:
        #    print(k)
        #print("DERP2")
        pass
    return res


#TODO: Remove from here. wrong module for this sort of thing
def single_player_get_data(id):
    def inner(m_id):
        m_d = match_detail.match_data_from_id(m_id)
        if m_d is None:
            return None
        in_map = match_detail.inter_map(m_d)
        player_data = match_detail.id_to_data(in_map,id,id_type='account_id',result_type='part_data')
        if player_data is None:
            return None
        return single_player_stats_wanted(player_data)
    return inner

def aggregation_function(init_map,aggregated_stats):
    res = {}
    if init_map is None:
        res = aggregated_stats
    else:
        for x in aggregated_stats:
            if x not in init_map:
                res[x] = aggregated_stats[x]
            else:
                res[x] = aggregated_stats[x] + init_map[x]
    return res

#   post_aggregation function : helper function
#
#
def post_aggregation(init_map,count_map):
    res = {}
    for x in init_map:
        res[x] = init_map[x] * 1.0 / count_map[x]
    return res

#   increment_count function : helper function
#   takes two inputs a count_map and a stat_map
#   the count map is a map data structure that whose values are the
#   number of times a certain key has occurred.
#   This function will increment the count map's values by 1
#   for each key that has occurred in stat_map.
#   Input: count_map, stat_map
#   Output: No output : count_map is incremented in place
def increment_count(count_map,stat_map):
    for s in stat_map:
        if s not in count_map:
            count_map[s] = 0
        count_map[s] += 1


#   stat_aggregate function : high-level function
#   over a list of matches, given a function that retrieves data from a match into a map
#   aggregate that data into a single map and averages it
#   input : m_l: list of match ids
#           required_data_func : function that retrieves wanted information from match id
#   output: average of stats in the required_data_func over all the matches
def stat_aggregate(m_l,required_data_func):
    res = None
    count_copy = {}
    for m in m_l:
        aggregated_stats = required_data_func(m)
        increment_count(count_copy,aggregated_stats)
        res = aggregation_function(res,aggregated_stats)
    res = post_aggregation(res,count_copy)
    return res



def sum_cs(p_li):
    res = 0
    for x in p_li:
        stats = x['stats']
        res += stats['totalMinionsKilled'] + stats['neutralMinionsKilled']
    return res

def sum_kills(p_li):
    res = 0
    for x in p_li:
        stats = x['stats']
        res += stats['kills']
    return res

def winrate_by_role_most_damage(m_l,acc_id_li):
    res = {}
    # map parts to roles
    # find out which part has the highest dmg
    # map that part to role, and in res, increment that one
    for m in m_l:
        m_d = match_detail.match_data_from_id(m)
        if m_d is None or gamepreds.is_remake()(m_d):
            continue
        in_map = match_detail.inter_map(m_d)
        for a in acc_id_li:
            t_id = match_detail.id_to_data(in_map,a,id_type='account_id',result_type='team_id')
            if t_id is not None:
                break
        team_part_ids = match_detail.id_to_data(in_map,t_id,id_type='team_id',result_type='parts_on_team')
        td = match_detail.id_to_data(in_map,t_id,id_type='team_id',result_type='team_data')
        max_dmg = 0
        max_role = ''
        for pid in team_part_ids:
            role = match_detail.id_to_data(in_map,pid,id_type='participant_id',result_type='role')
            pd = match_detail.id_to_data(in_map,pid,id_type='participant_id',result_type='part_data')
            dmg = pd['stats']['totalDamageDealtToChampions']
            if dmg > max_dmg:
                max_role = role
                max_dmg = dmg
        if max_role not in res:
            res[max_role] = [0,0]
            print(repr(max_role))
        won = td['win'] == 'Win'
        if won:
            res[max_role][0] += 1
        else:
            res[max_role][1] += 1
        if(max_role == u'NONE'):
            print(max_dmg)
    return res


def winrate_having_more_cs(m_l,acc_id_li):
    win,loss = 0,0
    for m in m_l:
        m_d = match_detail.match_data_from_id(m)
        if m_d is None:
            continue
        in_map = match_detail.inter_map(m_d)
        for a in acc_id_li:
            t_id = match_detail.id_to_data(in_map,a,id_type='account_id',result_type='team_id')
            if t_id is not None:
                break
        e_t_id = match_detail.enemy_team_id(in_map,t_id)
        team_part_data = match_detail.id_to_data(in_map,t_id,id_type='team_id',result_type='team_part_data')
        enemy_part_data = match_detail.id_to_data(in_map,e_t_id,id_type='team_id',result_type='team_part_data')
        td = match_detail.id_to_data(in_map,t_id,id_type='team_id',result_type='team_data')
        ally_cs = sum_cs(team_part_data)
        enemy_cs = sum_cs(enemy_part_data)
        won = td['win'] == 'Win'
        if ally_cs > enemy_cs:
            if won:
                win += 1
            else:
                loss += 1
    total = win + loss

    return round(win * 1.0 / total, 3)

def winrate_having_more_kills(m_l,acc_id_li):
    win,loss = 0,0
    for m in m_l:
        m_d = match_detail.match_data_from_id(m)
        if m_d is None:
            continue
        in_map = match_detail.inter_map(m_d)
        for a in acc_id_li:
            t_id = match_detail.id_to_data(in_map,a,id_type='account_id',result_type='team_id')
            if t_id is not None:
                break
        e_t_id = match_detail.enemy_team_id(in_map,t_id)
        team_part_data = match_detail.id_to_data(in_map,t_id,id_type='team_id',result_type='team_part_data')
        enemy_part_data = match_detail.id_to_data(in_map,e_t_id,id_type='team_id',result_type='team_part_data')
        td = match_detail.id_to_data(in_map,t_id,id_type='team_id',result_type='team_data')
        ally_kills = sum_kills(team_part_data)
        enemy_kills = sum_kills(enemy_part_data)
        won = td['win'] == 'Win'
        if won:
            if ally_kills > enemy_kills:
                win += 1
            else:
                loss += 1
    total = win + loss
    return round(win * 1.0 / total, 3)

def winrate_vs_all_champs(m_l,acc_id_li):
    res = {}
    for m in m_l:
        enemy_champs = []
        m_d = match_detail.match_data_from_id(m)
        if m_d is None:
            continue
        in_map = match_detail.inter_map(m_d)

        for a in acc_id_li:
            t_id = match_detail.id_to_data(in_map,a,id_type='account_id',result_type='team_id')
            if t_id is not None:
                break
        e_t_id = match_detail.enemy_team_id(in_map,t_id)
        enemy_part_data = match_detail.id_to_data(in_map,e_t_id,id_type='team_id',result_type='team_part_data')
        for p in enemy_part_data:
                enemy_champs.append(p['championId'])
        for c in enemy_champs:
            if c not in res:
                res[c] = [0,0]
        td = match_detail.id_to_data(in_map,t_id,id_type='team_id',result_type='team_data')
        won = td['win'] == 'Win'
        if won:
            for c in enemy_champs:
                 res[c][0] += 1
        else:
            for c in enemy_champs:
                res[c][1] += 1
    return res

if __name__ == "__main__":
    name_li = ['crysteenah','chulminyang','sbaneling']
    name_li += ['timbangu']
    name_li += ['starcalls coffee','ilovememundo','chulchultrain']
    name_li += ['bigheartjohnny','1000pingftw','inting griefer']
    name_li += ['thegoldenpenis']
    acc_id_li = name_to_acc.get_acc_id_for_group(name_li)
    #ft_pred = teampreds.team_cond(acc_id_li,teampreds.first_tower)
    win_pred = teampreds.team_cond(teampreds.team_cond_win)(acc_id_li)
    m_l = acc_to_matches.get_flex_match_list_for_group(acc_id_li)
    print(len(m_l))

    role_win_rate = winrate_by_role_most_damage(m_l,acc_id_li)
    for role in role_win_rate:
        print(role)
        win = role_win_rate[role][0]
        loss = role_win_rate[role][1]
        total = win + loss
        rate = round(win * 1.0 / total,3)
        print(win)
        print(loss)
        print(rate)
