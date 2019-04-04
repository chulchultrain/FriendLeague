import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'FriendLeague.settings'
import leagreq.league_curl as league_curl
import json
import django
from django.conf import settings
if __name__ == '__main__':
    django.setup()
from django.db import models
from analytics.models import Champion

# data_refresh function
# refreshs the data from riot API
# for champions
def data_refresh():
    data = league_curl.request('champion')['data']
    res = {}
    for x in data:
        #print(x)
        key = int(data[x]['key'])
        name = data[x]['name']
        #print(key)
        champ_data_str = json.dumps(data[x])
        o = Champion(champ_id = key,name=name,champ_data=data[x])
        o.save()
    cnx.commit()

# id_from_champion function
# Top Level Function
# input : champion_name : string
# output : champ_id : int/long
def id_from_champion(name):
    try:
        champ = Champion.objects.get(name=name)
        champ_id = champ.champ_id
    except DoesNotExist as e:
        print(e)
        champ_id = None
    return champ_id

# data_from_id function
# Top Level Function
# input : champion_id : int
# output : champion data structure from Riot API
def data_from_id(champ_id):
    try:
        champ = Champion.objects.get(champ_id = champ_id)
        data = champ.champ_data
        #print(data)
    except Champion.DoesNotExist as e:
        print(e)
        data = None
    return data

def name_from_id(champ_id):
    try:
        champ = Champion.objects.get(champ_id = champ_id)
        name = champ.name
    except Champion.DoesNotExist as e:
        print(e)
        name = None
    return name

# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    pass
def cleanup():
    pass

#testing function
def testing():
    assert(id_from_champion('Lux') == 99)
    assert(id_from_champion('Ahri') == 103)
    assert(data_from_id(99)['name'] == 'Lux')

if __name__ == '__main__':
    #data_refresh()
    testing()
