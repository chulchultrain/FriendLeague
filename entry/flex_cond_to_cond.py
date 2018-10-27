import leagreq.name_to_acc as name_to_acc
import leagreq.acc_to_matches as acc_to_matches
import stats.aggregation as aggregation
import preds.pred_translate as pred_translate
import sys
# Module serves as an entry point for a user to find common stats needed like
# a mapping of getting first tower to winrate
# or an average of performance statistics of a player over the players solo q or flex games
#
#
#

# TODO: Need a model
# One that stores the match_list to test on, and the account ids that are associated with the players
# whose stats we wish to calculate, and a set of predicates we wish to test
# maybe we dont need to keep the set of predicates, but definitely at least the match_lits and the account_ids

# TODO: Need to
#
#

def flex_cond_arg_parse(sys_args):
    try:
        cond_1 = sys_args[1]
        cond_2 = sys_args[2]
        name_li = sys_args[3:]
    except Exception as e:
        print("Usage: <cond_1> <cond_2> <name_1> <name_2> ... <name_n>")
    return cond_1,cond_2,name_li
def single_player(name,champion_name=None,lane=None):
    acc_id = name_to_acc.account_id_from_name(name)
    m_l = acc_to_matches.solo_q_matches(acc_id)
    print(len(m_l))
    data_func = aggregation.single_player_get_data(acc_id)
    res_map = aggregation.stat_aggregate(m_l,data_func)
    for x in res_map:
        print(str(x) + ":")
        print(res_map[x])

def flex_cond_to_cond(name_li,cond_1_str,cond_2_str):
    acc_id_li = name_to_acc.get_acc_id_for_group(name_li)
    cond_1 = pred_translate.translate(cond_1_str)(acc_id_li)
    cond_2 = pred_translate.translate(cond_2_str)(acc_id_li)
    if cond_1 is None or cond_2 is None:
        print("Either cond_1 or cond_2 are invalid conditions")
        print("Check the valid condition strings")
    m_l = acc_to_matches.get_flex_match_list_for_group(acc_id_li)
    aggregation.cond_to_cond(m_l,cond_1,cond_2)
if __name__ == "__main__":
    cond_1,cond_2,name_li = flex_cond_arg_parse(sys.argv)
    flex_cond_to_cond(name_li,cond_1,cond_2)
