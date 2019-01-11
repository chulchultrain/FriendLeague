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

def stat_aggregate(m_l,required_data_func,merge_in,):
    #count_copy = copy.deep_copy(data_points)
    #map_default_val(count_copy,0)
    #stats_so_far = copy.deep_copy(count_copy)
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
def single_player_get_data(account_id):
    def inner(m_id):
        m_d = match_detail.match_data_from_id(m_id)
        if m_d is None:
            return None
        in_map = match_detail.inter_map(m_d)
        player_data = match_detail.id_to_data(in_map,account_id,id_type='account_id',result_type='part_data')
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



if __name__ == "__main__":
    name_li = ['crysteenah','chulminyang','sbaneling']
    name_li += ['blanket robber']
    name_li += ['starcalls coffee','ilovememundo','chulchultrain']
    name_li += ['bigheartjohnny','FlexMasterJohnny']
    name_li += ['thegoldenpenis']
    cnx = league_util.conn_postgre()
    cursor = cnx.cursor()
    acc_id_li = name_to_acc.get_acc_id_for_group(name_li,cursor)
    #ft_pred = teampreds.team_cond(acc_id_li,teampreds.first_tower)
    win_pred = teampreds.team_cond(teampreds.team_cond_win)(acc_id_li)
    m_l = acc_to_matches.get_flex_match_list_for_group(acc_id_li,True,cursor)
    print(len(m_l))
