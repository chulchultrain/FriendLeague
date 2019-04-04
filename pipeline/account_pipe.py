#
#   Data pipeline for refreshing account's aggregate data table
#
#   For each match, make it into a <k,v> pair where key is account_id
#   where account_id already exists in our table of accounts
#   and val is the player_data.
#   Group all matches with a certain key into a collection.
#   For each key, process all of its values.
#   We want to take out key data items for player data,
#   For each key, we want to group these player data further by champion id.
#   keeping a map of champion_id to data.
#   and for each champion_id keep a count of games.
#   Then, we will merge them into the Aggregate_Account table at the end.


def gen_kv_map(match_id_li):
    pass

def process_kv_map()

def account_pipeline(match_id_li):
    #for each m_id, create key,value pairs between account_id and match_id(a space saving optimization on player_data)
    #Group all key,value pairs by key into a collection.
    #For each key, process all of its values(the player data in the match)
    #For each key, merge the resulting data into aggregate_account
    kv_li_map = gen_kv_map(match_id_li)
    res_data_map = process_kv_map(kv_li_map)
    merge_data(res_data_map)
