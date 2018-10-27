import leagreq.match_detail as match_detail
import leagreq.name_to_acc as name_to_acc
import leagreq.acc_to_matches as acc_to_matches
import leagreq.champ_detail as champ_detail
import sets
import preds.teampreds as teampreds
import preds.gamepreds as gamepreds
import preds.playerpreds as playerpreds
import decimal
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

x = 1
def single_player_stats_wanted(part_data):
    res = {}
    p_d = part_data['stats']
    res['cs'] = p_d['totalMinionsKilled'] + p_d['neutralMinionsKilled']

    res['kills'] = p_d['kills']
    res['deaths'] = p_d['deaths']
    res['damage'] = p_d['totalDamageDealtToChampions']
    res['assists'] = p_d['assists']
    p_t = part_data['timeline']
    print(p_t['lane'],p_t['role'],part_data['championId'])
    return res



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

#statistics for configurations

def post_aggregation(init_map,total):
    res = {}
    for x in init_map:
        res[x] = init_map[x] * 1.0 / total
    return res

def stat_aggregate(m_l,get_required_data_func):
    res = None
    for m in m_l:
        aggregated_stats = get_required_data_func(m)
        res = aggregation_function(res,aggregated_stats)
    res = post_aggregation(res,len(m_l))
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
        if m_d is None or gamepreds.is_remake(m_d):
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

def rift_win_rate(m_l,acc_id_li):
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
        td = match_detail.id_to_data(in_map,t_id,id_type='team_id',result_type='team_data')
        got_rift = td['firstRiftHerald']
        won = td['win'] == 'Win'
        if won:
            if got_rift:
                win += 1
            else:
                loss += 1
    total = win + loss
    return round(win * 1.0 / total, 3)

def baron_win_rate(m_l,acc_id_li):
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
        td = match_detail.id_to_data(in_map,t_id,id_type='team_id',result_type='team_data')
        got_rift = td['firstBaron']
        won = td['win'] == 'Win'
        if got_rift == False:
            if won:
                win += 1
            else:
                loss += 1
    total = win + loss
    print(win)
    print(loss)
    return round(win * 1.0 / total, 3)

def rift_win_rate(m_l,acc_id_li):
    win,loss = 0,0
    we_got_rift,they_got_rift = 0,0
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
        td = match_detail.id_to_data(in_map,t_id,id_type='team_id',result_type='team_data')
        e_td = match_detail.id_to_data(in_map,e_t_id,id_type='team_id',result_type='team_data')
        got_rift = td['firstRiftHerald']
        enemy_got_rift = e_td['firstRiftHerald']
        won = td['win'] == 'Win'
        if got_rift:
            we_got_rift += 1
        if enemy_got_rift:
            they_got_rift += 1
        if enemy_got_rift == False and got_rift == False:
            if won:
                win += 1
            else:
                loss += 1
    total = win + loss
    print(we_got_rift)
    print(they_got_rift)
    print(win)
    print(loss)
    return round(win * 1.0 / total, 3)

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
    #print(cond_to_cond(m_l,ft_pred,win_pred))
    #TODO: w/r by time length



    #res = winrate_vs_all_champs(m_l,acc_id_li)
    #print(len(res))
    #res_li = []
    #for c in res:
    #    #print(c)
    #    c_n = champ_detail.data_from_id(c)['name']
    #    win = res[c][0]
    #    loss = res[c][1]
    #    total = win + loss
    #    res_li.append([c_n,win,loss,round(win * 1.0 / total,3)])

    #sorted_li = sorted(res_li, key = (lambda x : x[3]))
    #for x in sorted_li:
    #    print(x[0] + ' ' + str(x[1]) + ' ' + str(x[2]) + ' ' + str(x[3]))

    #i = 1
    #print(winrate_having_more_cs(m_l,acc_id_li))
    #print(winrate_having_more_kills(m_l,acc_id_li))
    #print(rift_win_rate(m_l,acc_id_li))

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

    #while i < 5:
    #    print("winrate for " + str(i))
    #    match_len = gamepreds.game_len_int_cond(i * 600, (i + 1) * 600)
    #    gm = gamepreds.game_cond(match_len)
    #    print(cond_to_cond(m_l,gm,win_pred))
    #    i += 1
    #for name in name_li:
        #print("WIN RATE FOR FIRSTBLOOD on " + name)
        #acc_id = name_to_acc.account_id_from_name(name)
        #got_first_blood = playerpreds.player_cond(acc_id,playerpreds.got_first_blood())
        #print(cond_to_cond(m_l,got_first_blood,win_pred))
