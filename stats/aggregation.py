import leagreq.match_detail as match_detail
import leagreq.name_to_acc as name_to_acc
import leagreq.acc_to_matches as acc_to_matches
import leagreq.champ_detail as champ_detail
#
#given a set of matches for an id, calculate performance statistics for that player on that set of games
#i want cs diff against other laner.


#initially, we'll do cs score, avg gold, avg kills, deaths, assists see these things arent too useful due to some games being longer than others
#

def playschamp(match_general,champion_name):
    champ_id = champ_detail.id_from_champion(champion_name)
#    print(champ_id)
#    print(match_general['champion'])
    #if champ_id == match_general['champion']:
#        print("YES")#
#    else:
#        print("NO")
    return match_general['champion'] == champ_id

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


def calc_champ_stats(summoner_name,champion_name):
    acc_id = name_to_acc.account_id_from_name(summoner_name)
    total_match_list = acc_to_matches.matches_from_id(acc_id)
    filtered_match_list = []
    for m in total_match_list:
        if playschamp(m,champion_name):
            filtered_match_list.append(m)
    res = aggregate_statistics(filtered_match_list,acc_id)
    #print(len(filtered_match_list))
    print("Over " + str(len(filtered_match_list)) + " games, " + summoner_name + "'s average performance on " + champion_name + ":")
    for m in res:
        print(m + ': ' + str(res[m]))
    return res

def side_by_side(pref1,pref2):
    stats1 = calc_champ_stats(pref1[0],pref1[1])
    stats2 = calc_champ_stats(pref2[0],pref2[1])


calc_champ_stats('crysteenah','Lux')
calc_champ_stats('chulminyang','Gangplank')
