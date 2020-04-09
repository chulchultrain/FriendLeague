import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'FriendLeague.settings'

import django
from django.conf import settings
if __name__ == '__main__':
    django.setup()
import leagreq.match as match
from django.db import models
from analytics.models import Match_Summary, Champion


def retrieve_match_data(match_id):
    return match.match_data_from_id(match_id)

def retrieve_match_summary(match_id):
    match_summary = None
    try:
        match = Match_Summary.objects.get(pk = match_id)
        match_summary = match.match_summary
    except Match_Summary.DoesNotExist as e:
        print(e)
        match_summary = None
    return match_summary

def match_summary_from_data(match_data):
    match_summary = {}
    player_map = {}
    p_i_data = match_data['participantIdentities']
    #get map of participant ids to summoner names
    for participant_dto in p_i_data:
        pid = participant_dto['participantId']
        player_dto = participant_dto['player']
        name = player_dto['summonerName']
        player_map[pid] = name
    #main data structure: map team ids to a list of players
    team_li = match_data['teams']

    for team_stats_dto in team_li:
        team_id = team_stats_dto['teamId']
        match_summary[team_id] = {}
    participants = match_data['participants']
    for participant in participants:
        pid = participant['participantId']
        #TODO: get champion id and champion name and put into the stat obj so that we can display it on the site
        champion_name = None
        try:
            champion_name = Champion.objects.get(pk=participant['championId']).name
        except Champion.DoesNotExist as e:
            print(e)
            champion_name = None
        stats = participant['stats']
        team_id = participant['teamId']
        stat_obj = {}
        stat_obj['name'] = player_map[pid]
        stat_obj['champion_name'] = champion_name
        stat_obj['cs'] = stats['totalMinionsKilled'] + stats['neutralMinionsKilled']
        stat_obj['wards_placed'] = stats['wardsPlaced']
        stat_obj['wards_killed'] = stats['wardsKilled']
        stat_obj['vision_wards'] = stats['visionWardsBoughtInGame']
        stat_obj['kills'] = stats['kills']
        stat_obj['deaths'] = stats['deaths']
        stat_obj['damage'] = stats['totalDamageDealtToChampions']
        stat_obj['assists'] = stats['assists']
        if pid not in match_summary[team_id]:
            match_summary[team_id][pid] = stat_obj
    #for each player in the list of players, map player to pertinent statistics data
    return match_summary

def insert_match_summary(match_id,match_summary):
    try:
        m = Match_Summary(pk=match_id,match_summary=match_summary)
        m.save()
    except Exception as e:
        print(e)

def match_summary_refresh(match_id):
    m_d = retrieve_match_data(match_id)
    m_s = match_summary_from_data(m_d)
    if m_s is None:
        print("could not create match summary for match id {0}".format(match_id))
    else:
        insert_match_summary(match_id,m_s)
    return m_s

def match_summary_from_id(match_id):
    m_s = retrieve_match_summary(match_id)
    if m_s is None:
        m_s = match_summary_refresh(match_id)
    return m_s


if __name__ == '__main__':
    m_li = [3261183035, 3261153950, 3261099177, 3261062565, 3261042120]
    for m in m_li:
        match_summary_from_id(m)
