import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'FriendLeague.settings'
import leagreq.league_curl as league_curl
import utils.league_util as league_util
import datetime
import django
from django.conf import settings
if __name__ == '__main__':
    django.setup()
from django.db import models
from analytics.models import Account

#   Will map accounts to the list of match data.
#
#   Instead of refreshing the entire list everytime, which will take up network bandwidith.
#   We keep track of when the last time the matchdata was refreshed for each account we have on hand.
#


# request_remaining_games function
# calls the Riot API to get a list of all the new matches that an
# account has played after the timestamp associated with that account id
# inside our acc_refresh_timestamp map
def request_remaining_games(id,beginTime=0):
    cur_match = 0
    cur_season = 11
    param_map = {'beginTime':beginTime,'beginIndex':cur_match}
    param_map['seasonId'] = 11 #TODO: put in leagueconf
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
def refresh_matches(id):
    res_match_data = []
    last_timestamp = get_refresh_timestamp(id)
    new_matches = request_remaining_games(id,last_timestamp)
    #try to secure write lock on the id. try to atomic commit
    set_refresh_timestamp(id)
    insert_matches(id,new_matches)
    #unlock
    if new_matches is None:
        raise RuntimeError("Couldn't retrieve match data for the account id " + str(id))

    return new_matches


def get_refresh_timestamp(account_id):
    try:
        acc = Account.objects.get(account_id = account_id)
        refresh = acc.refresh
        refresh = league_util.dt_to_riot_timestamp(refresh)
    except Account.DoesNotExist as e:
        refresh = 0
    return refresh

def set_refresh_timestamp(account_id):
    #insert_if_DNE(id,cursor)
    try:
        acc = Account.objects.get(account_id = account_id)
        acc.refresh = datetime.datetime.now()
        acc.save()
    except Account.DoesNotExist as e:
        print(e)

def insert_matches(account_id,match_gen_list):
    solo_matches = []
    flex_matches = []
    for m in match_gen_list:
        if is_solo_match(m):
            solo_matches.append(m['gameId'])
        elif is_flex_match(m):
            flex_matches.append(m['gameId'])
    try:
        acc = Account.objects.get(account_id = account_id)
        acc.solo_match_list += solo_matches
        acc.flex_match_list += flex_matches
        acc.save()
    except Account.DoesNotExist as e:
        print(e)

def get_existing_matches(account_id,queue=None):
    res = []
    try:
        acc = Account.objects.get(account_id = account_id)
        if queue is 'solo':
            res += acc.solo_match_list
        elif queue is 'flex':
            res += acc.flex_match_list
        elif queue is None:
            res += acc.solo_match_list + acc.flex_match_list
    except Account.DoesNotExist as e:
        print(e)
    return res


# is a solo q match predicate : takes match general data strcture
def is_solo_match(match):
    return match['queue'] == 420

# is a flex q match predicate : takes match general data structure
def is_flex_match(match):
    return match['queue'] == 440

def all_matches(id,refresh_flag=False):
    if(refresh_flag):
        refresh_matches(id)
    res = get_existing_matches(id)
    return res

# solo_q_matches function
# Top Level Function
# gets all solo queue matches for a given id
# by filtering on all the matches for the solo queue type
# and takes a refresh flag to indicate whether to call Riot API for more matches
def solo_q_matches(id, refresh_flag = False):
    if(refresh_flag):
        refresh_matches(id)
    res = get_existing_matches(id,queue='solo')
    return res


# flex_q_matches function
# Top Level Function
# gets all flex queue matches for a given id
# by filtering on all the matches for the flex queue type
# and takes a refresh flag to indicate whether to call Riot API for more matches
def flex_q_matches(name,refresh_flag = False):
    if(refresh_flag):
        refresh_matches(id)
    res = get_existing_matches(id,queue='flex')
    return res

#TODO: A SOLO Q COUNTERPART TO get_flex_match_list_for_group

# get_flex_match_list_for_group function
# Top Level Function
# gets all flex queue matches that had at least one person from a list of people
# in a single list
# takes a refresh flag to indicate whether to call Riot API for more matches
# acc_id_li : List[Int/Long]
# refresh_flag : Boolean
def get_flex_match_list_for_group(acc_name_li,refresh_flag = False):
    init_filter = []
    id_set = set()
    for a in acc_name_li:
        m_li = flex_q_matches(a,refresh_flag)
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
    print(solo_q_matches('bvw_nI2IATn8zNJosGoqNacUFUURmWRjMy-mrbWksN75gw',refresh_flag=True))
    print("NO ASSERTS FOR THSI MODULE")
setup()
if __name__ == "__main__":
    testing()
cleanup()
