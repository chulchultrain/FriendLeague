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
#




#implement custom aggregation. can choose w/e stats you want, and aggregate in different ways if want.


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


def team_cond(acc_id_li,team_cond_predicate):
    #get id. get part id. get team id. check if that team took first drag

    def inner(m_d):
        for a in acc_id_li:
            part_id = match_detail.find_part_id(m_d,a) #can optimize for inner loop repetition later
            if part_id is not None:
                break
        #part_id = match_detail.find_part_id(m_d,acc_id)
        t_d = match_detail.team_data(m_d,part_id)
        return team_cond_predicate(t_d)
    return inner


def cond_to_successrate(match_set,cond_predicate,success_predicate):
    win,loss = 0,0
    for m in match_set:
        mid = m['gameId']
        md = match_detail.match_data_from_id(mid)
        if cond_predicate(md):
            if success_predicate(md):
                win += 1
            else:
                loss += 1
    total = win + loss
    print(str(win) + ' ' + str(loss))
    return win * 1.0 / total * 1.0



#calc_champ_lane_stats('crysteenah','Lux','MIDDLE')
#calc_champ_lane_stats('chulminyang','Gangplank','TOP')


#get list of players, get flex q matches,
#
#

#shit needs to be in name_to_acc



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
#print(group_cond_to_cond(name_li,first_drag,team_cond_win))
print(group_cond_to_cond(name_li,teampreds.first_tower,teampreds.team_cond_win))
