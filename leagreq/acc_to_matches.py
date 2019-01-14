import leagreq.league_curl as league_curl
import league_conf
import pickle
import subprocess
import utils.league_util as league_util
import utils.filemap as filemap

#   Will map accounts to the list of match data.
#
#   Instead of refreshing the entire list everytime, which will take up network bandwidith.
#   We keep track of when the last time the matchdata was refreshed for each account we have on hand.
#


# request_remaining_games function
# calls the Riot API to get a list of all the new matches that an
# account has played after the timestamp associated with that account id
# inside our acc_refresh_timestamp map
def request_remaining_games(id,cursor,beginTime=0):
    cur_match = 0
    cur_season = 11
    param_map = {'beginTime':beginTime,'beginIndex':cur_match}
    param_map['seasonId'] = 11
    acc_match_data = league_curl.request('match_list',id,param_map)
    matches = []
    while(acc_match_data is not None and cur_match  < acc_match_data['totalGames']):
        matches += acc_match_data['matches']
        cur_match += 100
        param_map['beginIndex'] = cur_match
        acc_match_data = league_curl.request('match_list',id,param_map)
    print(len(matches))
    return matches

# matches_refresh function
# low level function
# updates both the match_list for an id and the timestamp for when the last
# set of games was pulled
def refresh_matches(id,cursor):

    res_match_data = []
    last_timestamp = get_refresh_timestamp(id,cursor)
    new_matches = request_remaining_games(id,cursor,last_timestamp)
    #try to secure write lock on the id. try to atomic commit
    set_refresh_timestamp(id,cursor)
    insert_matches(id,cursor,new_matches)
    #unloc
    if new_matches is None:
        raise RuntimeError("Couldn't retrieve match data for the account id " + str(id))

    return new_matches


def get_refresh_timestamp(id,cursor):
    cursor.execute('select refresh from analytics_account where account_id = %s',[id])
    refresh = 0
    refresh = cursor.fetchone()
    refresh = refresh[0]
    refresh = league_util.dt_to_riot_timestamp(refresh)
    print(refresh)
    return refresh

def set_refresh_timestamp(id,cursor):
    #insert_if_DNE(id,cursor)
    cursor.execute('update analytics_account set refresh = now() where account_id = %s',[id])

# matches_from_id function
# Top level function
# returns the list of match ids associated with an account id
# takes a refresh_flag to indicate whether we want to call the Riot API to get more matches

def insert_matches(id,cursor,match_gen_list):
    solo_matches = []
    flex_matches = []
    for m in match_gen_list:
        if is_solo_match(m):
            solo_matches.append(m['gameId'])
        elif is_flex_match(m):
            flex_matches.append(m['gameId'])

    stmt = 'update analytics_account set {0}=array_cat({0},%s::bigint[]) where account_id = %s'
    solo_update = stmt.format('solo_match_list')
    flex_update = stmt.format('flex_match_list')
    print(solo_update)
    cursor.execute(solo_update,[solo_matches,id])
    cursor.execute(flex_update,[flex_matches,id])
    cnx = cursor.connection
    cnx.commit()



def get_existing_matches(id,cursor=None,queue=None):
    stmt = 'select {0}_match_list from analytics_account where account_id = %s'
    params = [id]
    if queue is not None:
        retrieve = stmt.format(queue)
        cursor.execute(retrieve,[id])
    elif queue is None:
        get_existing_matches(id,cursor,'solo') + get_existing_matches(id,cursor,'flex')
    m_l = []
    for c in cursor:
        m_l += c[0]
    return m_l



# is a solo q match predicate : takes match general data strcture
def is_solo_match(match):
    return match['queue'] == 420

# is a flex q match predicate : takes match general data structure
def is_flex_match(match):
    return match['queue'] == 440

def all_matches(id,refresh_flag=False,cursor=None):
    if(refresh_flag):
        refresh_matches(id,cursor)
    res = get_existing_matches(id,cursor)
    return res

# solo_q_matches function
# Top Level Function
# gets all solo queue matches for a given id
# by filtering on all the matches for the solo queue type
# and takes a refresh flag to indicate whether to call Riot API for more matches
def solo_q_matches(id, refresh_flag = False,cursor=None):
    if(refresh_flag):
        refresh_matches(id,cursor)
    res = get_existing_matches(id,cursor,queue='solo')
    return res


# flex_q_matches function
# Top Level Function
# gets all flex queue matches for a given id
# by filtering on all the matches for the flex queue type
# and takes a refresh flag to indicate whether to call Riot API for more matches
def flex_q_matches(name,refresh_flag = False,cursor=None):
    if(refresh_flag):
        refresh_matches(id,cursor)
    res = get_existing_matches(id,cursor,queue='flex')
    return res

#TODO: A SOLO Q COUNTERPART TO get_flex_match_list_for_group

# get_flex_match_list_for_group function
# Top Level Function
# gets all flex queue matches that had at least one person from a list of people
# in a single list
# takes a refresh flag to indicate whether to call Riot API for more matches
# acc_id_li : List[Int/Long]
# refresh_flag : Boolean
def get_flex_match_list_for_group(acc_name_li,refresh_flag = False,cursor=None):
    init_filter = []
    id_set = set()
    for a in acc_name_li:
        m_li = flex_q_matches(a,refresh_flag,cursor)
        for m in m_li:
            if m not in id_set:
                init_filter.append(m)
                id_set.add(m)
    return init_filter

# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    pass

# cleanup function
# does all necessary tasks at the end of the script to use the module correctly
# and save results from processing
# Note: Should really be called at the end of the caller scripts life.
def cleanup():
    pass

#get matches with filter.
#get matches for list with filter
#with flag to refresh

def testing():
    #print(new_matches_from_id(44649467))
    #print(matches_from_id(44649467))
    with league_util.conn_postgre() as cnx:
        with cnx.cursor() as cursor:
            print(solo_q_matches('bvw_nI2IATn8zNJosGoqNacUFUURmWRjMy-mrbWksN75gw',refresh_flag=True,cursor=cursor))
    print("NO ASSERTS FOR THSI MODULE")
setup()
if __name__ == "__main__":
    testing()
cleanup()
