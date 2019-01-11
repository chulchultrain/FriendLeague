import utils.league_util as league_util
import leagreq.name_to_acc as name_to_acc
import leagreq.acc_to_matches as acc_to_matches
import leagreq.match_detail as match_detail

def load_into_db(req_type=None,req_id=None,cursor=None):
    # get account from name and load account details into account
    # get refreshed match_list from id and load new matches into account
    # get a match_detail from match_id and load into match_detail
    if req_type is 'account':
        name_to_acc.account_id_from_name(req_id,cursor)
    elif req_type is 'match_list':
        acc_to_matches.all_matches(req_id,refresh_flag=True,cursor=cursor)
    elif req_type is 'match_detail':
        match_detail.match_data_from_id(req_id,cursor)
