import leagreq.name_to_acc as name_to_acc
import leagreq.acc_to_matches as acc_to_matches
import stats.aggregation as aggregation
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

def single_player(name):
    acc_id = name_to_acc.account_id_from_name(name)
    m_l = acc_to_matches.solo_q_matches(acc_id)
    print(len(m_l))
    data_func = aggregation.single_player_get_data(acc_id)
    res_map = aggregation.stat_aggregate(m_l,data_func)
    for x in res_map:
        print(str(x) + ":")
        print(res_map[x])


if __name__ == "__main__":
    name = sys.argv[1]
    single_player(name)
