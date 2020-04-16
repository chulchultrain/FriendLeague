import leagreq.name_to_acc as name_to_acc
import leagreq.acc_to_matches as acc_to_matches
import stats.aggregation as aggregation
import preds.pred_translate as pred_translate
import preds.playerpreds as playerpreds
import preds.gamepreds as gamepreds
import sys
import argparse
# Module serves as an entry point for a user to find common stats needed like
# a mapping of getting first tower to winrate
# or an average of performance statistics of a player over the players solo q or flex games

# TODO: Need a model - but do we really?
# One that stores the match_list to test on, and the account ids that are associated with the players
# whose stats we wish to calculate, and a set of predicates we wish to test
# maybe we dont need to keep the set of predicates, but definitely at least the match_lits and the account_ids

#   parses the sys args that are passed in through the command line
#   input: sys_args : sys.argv thats passed in from command line
#   output: name,champion,role : 3-string tuple
def solo_cond_arg_parse(sys_args):
    parser = argparse.ArgumentParser()
    parser.add_argument("name",help = "the name of the summoner")
    parser.add_argument('-c',"--champion",help = "the name of the champion")
    parser.add_argument('-l',"--lane",help = "the role. Valid: TOP MIDDLE BOTTOM SUPPORT JUNGLE")
    args = parser.parse_args()
    name = args.name
    champion = args.champion
    role = args.lane
    print(name,champion,role)
    return name,champion,role

#   single_player function - high-level function
#   This function will take in a summoner name, a champion_name(optional), and a role(optional)
#   It will print that players stats on all the solo q matches given that
#   the player played that champion and/or that role, provided the criteria was provided
#   input: name : string
#          champion_name : string
#          lane : string
#   output: None : will print players stats on single-player
def single_player(name,champion_name=None,lane=None):
    acc_id = name_to_acc.account_id_from_name(name)
    m_l = acc_to_matches.solo_q_matches(acc_id)
    filtered_m_l = []
    cr_pred = playerpreds.champ_role(champ_name=champion_name,role=lane)
    champ_role_pred = playerpreds.player_cond(acc_id,cr_pred)
    remake_pred = gamepreds.game_cond(gamepreds.is_remake())
    for m in m_l:
        if remake_pred(m) is False and champ_role_pred(m):
            filtered_m_l.append(m)
    print(len(filtered_m_l))
    data_func = aggregation.single_player_get_data(acc_id)
    res_map = aggregation.stat_aggregate(filtered_m_l,data_func)
    for x in res_map:
        print(str(x) + ":")
        print(res_map[x])
    return res_map

if __name__ == "__main__":
    name,champion,role = solo_cond_arg_parse(sys.argv)
    single_player(name,champion_name=champion,lane=role)
