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





#statistics for configurations

def stat_aggregate(m_l,get_required_data_func,aggregation_function):
    res = None
    for m in m_l:
        m_d = match_detail.match_data_from_id(m)
        aggregated_stats = get_required_data_func(m_d)
        res = aggregation_function(res,aggregated_stats)
    return res

def winrate_vs_all_champs(m_l,acc_id_li):
    res = {}
    team_win_cond = teampreds.team_cond(acc_id_li,teampreds.team_cond_win)
    for m in m_l:
        enemy_champs = []
        m_d = match_detail.match_data_from_id(m)
        if m_d is None:
            continue
        enemy_t_id = match_detail.find_other_team_from_id_li(m_d,acc_id_li)
        #if enemy_t_id is None:
        #    continue
        #print(enemy_t_id)
        for p in m_d['participants']:
            if p['teamId'] == enemy_t_id:
                enemy_champs.append(p['championId'])
        #print(m)
        #print(enemy_champs)
        for c in enemy_champs:
            if c not in res:
                res[c] = [0,0]
        if team_win_cond(m):
            for c in enemy_champs:
                 res[c][0] += 1
        else:
            for c in enemy_champs:
                res[c][1] += 1
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
print(len(m_l))
#print(cond_to_cond(m_l,ft_pred,win_pred))
#TODO: w/r by time length



res = winrate_vs_all_champs(m_l,acc_id_li)
print(len(res))
res_li = []
for c in res:
    #print(c)
    c_n = champ_detail.data_from_id(c)['name']
    win = res[c][0]
    loss = res[c][1]
    total = win + loss
    res_li.append([c_n,win,loss,round(win * 1.0 / total,3)])

sorted_li = sorted(res_li, key = (lambda x : x[3]))
for x in sorted_li:
    print(x[0] + ' ' + str(x[1]) + ' ' + str(x[2]) + ' ' + str(x[3]))

i = 1
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
