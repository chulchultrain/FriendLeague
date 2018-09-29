import leagreq.match_detail as match_detail
import leagreq.name_to_acc as name_to_acc
import leagreq.acc_to_matches as acc_to_matches
import leagreq.champ_detail as champ_detail
import sets
import preds.teampreds as teampreds
import preds.gamepreds as gamepreds
import preds.playerpreds as playerpreds
#
#given a set of matches for an id, calculate performance statistics for that player on that set of games
#i want cs diff against other laner.


#initially, we'll do cs score, avg gold, avg kills, deaths, assists see these things arent too useful due to some games being longer than others
#implement custom aggregation. can choose w/e stats you want, and aggregate in different ways if want.

# custom aggregation
# what i want is to be able to choose w/e stats i want
# how can i choose the custom stats because its a map, should i keep a map
# of things to be added?
#
#
def add_to_aggregate(aggregate,m):
    for key in m:
        if key not in aggregate:
            aggregate[key] = 0
        aggregate[key] += m[key]

def keep_data(player_data):
    stats = player_data['stats']
    res = {}
    res['cs'] = stats['totalMinionsKilled'] + stats['neutralMinionsKilled']
    res['gold'] = stats['goldEarned']
    res['kills'] = stats['kills']
    res['deaths'] = stats['deaths']
    res['assists'] = stats['assists']
    return res
def include_in_aggregate(aggregate,player_data):
    include_data = keep_data(player_data)
    add_to_aggregate(aggregate,include_data)

def calculate_aggregates(m,sample_size):
    res = {}
    for key in m:
        res[key] = m[key] * 1.0 / sample_size
    return res

def aggregate_statistics(match_set,id):
    res = {}
    for m in match_set:
        mid = m['gameId']
        md = match_detail.match_data_from_id(mid)
        pd = match_detail.player_data_from_match(md,id)
        include_in_aggregate(res,pd)
    res = calculate_aggregates(res,len(match_set))
    return res



#calc_champ_lane_stats('crysteenah','Lux','MIDDLE')
#calc_champ_lane_stats('chulminyang','Gangplank','TOP')


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




def group_cond_to_cond(name_li,cond_pred,success_pred):
    acc_id_li = name_to_acc.get_acc_id_for_group(name_li)
    m_li = acc_to_matches.get_flex_match_list_for_group(acc_id_li)
    success,failure = 0,0
    team_init_cond = team_cond(acc_id_li,cond_pred)
    team_success_cond = team_cond(acc_id_li,success_pred)
    for m in m_li:
        md = match_detail.match_data_from_id(m['gameId'])
        if md is None:
            continue
        if gamepreds.is_remake(md) is False and team_init_cond(md):
            if team_success_cond(md):
                success += 1
            else:
                failure += 1
    total = success + failure
    print("Total games for this run:")
    print(total)
    print(success)
    print(failure)
    return success * 1.0 / total * 1.0


def calc_champ_lane_stats(summoner_name,champion_name,lane):
    acc_id = name_to_acc.account_id_from_name(summoner_name)
    total_match_list = acc_to_matches.matches_from_id(acc_id)
    filtered_match_list = []
    champ_pred = plays_champ(champion_name)
    lane_pred = is_lane(lane)
    for m in total_match_list:
        if champ_pred(m) and lane_pred(m):
            filtered_match_list.append(m)
    print("FINISHED FILTERING MATCHES")
    res = aggregate_statistics(filtered_match_list,acc_id)
    #print(len(filtered_match_list))
    print("Over " + str(len(filtered_match_list)) + " games, " + summoner_name + "'s average performance on " + champion_name + ":")
    for m in res:
        print(m + ': ' + str(res[m]))
    return res


name_li = ['crysteenah','chulminyang','sbaneling']
name_li += ['timbangu']
name_li += ['starcalls coffee','ilovememundo','chulchultrain']
name_li += ['bigheartjohnny','1000pingftw','inting griefer']
name_li += ['thegoldenpenis']
acc_id_li = name_to_acc.get_acc_id_for_group(name_li)
#ft_pred = teampreds.team_cond(acc_id_li,teampreds.first_tower)
win_pred = teampreds.team_cond(acc_id_li,teampreds.team_cond_win)
m_l = acc_to_matches.get_flex_match_list_for_group(acc_id_li)
#print(cond_to_cond(m_l,ft_pred,win_pred))
#TODO: w/r by time length

i = 1
while i < 5:
    print("winrate for " + str(i))
    match_len = gamepreds.game_len_int_cond(i * 600, (i + 1) * 600)
    gm = gamepreds.game_cond(match_len)
    print(cond_to_cond(m_l,gm,win_pred))
    i += 1
#for name in name_li:
    #print("WIN RATE FOR FIRSTBLOOD on " + name)
    #acc_id = name_to_acc.account_id_from_name(name)
    #got_first_blood = playerpreds.player_cond(acc_id,playerpreds.got_first_blood())
    #print(cond_to_cond(m_l,got_first_blood,win_pred))
