import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'FriendLeague.settings'

import django
from django.conf import settings
if __name__ == '__main__':
    django.setup()
import leagreq.league_curl as league_curl
from django.db import models
from analytics.models import Match_Detail

# match_data_refresh function
# low level function
# makes a request to the Riot API for the desired match data
# given the match id.
def match_data_refresh(match_id):
    match_data = league_curl.request('match',match_id)
    if match_id is None:
        print("COULDNT FIND MATCH " + str(match_id))
        return None
    return match_data

#   try to retrieve match data from our database
#   return None is does not exist
def retrieve_match_data(match_id):
    match_data = None
    try:
        match = Match_Detail.objects.get(pk = match_id)
        match_data = match.match_data
    except Match_Detail.DoesNotExist as e:
        print(e)
        match_data = None
    return match_data

def insert_match_data(match_id,match_data):
    #TODO:
    try:
        m = Match_Detail(pk=match_id,match_data=match_data)
        m.save()
    except Exception as e:
        print(e)


# match_data_from_id function
# high level function
# this function returns the desired match data given a match id.
def match_data_from_id(match_id):
    match_data = retrieve_match_data(match_id)
    if match_data is None:
        match_data = match_data_refresh(match_id)
        if match_data is None:
            print("Could not find data for match {0}".format(match_id))
        else:
            insert_match_data(match_id,match_data)
    return match_data


# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    pass

# cleanup function
# does all necessary tasks at the end of the script to use the module correctly
def cleanup():
    pass

def testing():
        r = match_data_from_id(2859270267)
        print(r)


setup()
if __name__ == '__main__':
    testing()
cleanup()
