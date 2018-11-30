import leagreq.name_to_acc as name_to_acc
import leagreq.acc_to_matches as acc_to_matches
import stats.aggregation as aggregation
import preds.pred_translate as pred_translate
import sys
import argparse
# Module serves as an entry point for finding the rate of which
# a condition is true given another condition within the flex games
# of a list of players
#

# TODO: Need a model
# One that stores the match_list to test on, and the account ids that are associated with the players
# whose stats we wish to calculate, and a set of predicates we wish to test
# maybe we dont need to keep the set of predicates, but definitely at least the match_lits and the account_ids


def flex_cond_arg_parse(sys_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--names',nargs='+',help='the names of summoners',required=True)
    parser.add_argument('--cond1',required=True)
    parser.add_argument('--cond2',required=True)
    args = parser.parse_args()
    return args.cond1,args.cond2,args.names
def single_player(name,champion_name=None,lane=None):
    acc_id = name_to_acc.account_id_from_name(name)
    m_l = acc_to_matches.solo_q_matches(acc_id)
    print(len(m_l))
    data_func = aggregation.single_player_get_data(acc_id)
    res_map = aggregation.stat_aggregate(m_l,data_func)
    for x in res_map:
        print(str(x) + ":")
        print(res_map[x])
# flex_cond_to_cond function - high-level function
# this function will calculate the rate at which the 2nd condition is true
# given the first condition over the set of flex games played by the players
# in the name list
# input : name_li : list[string]
#         cond_1_str : string
#         cond_2_str : string
# valid cond_strings are defined in the preds.pred_translate module
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
