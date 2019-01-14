import leagreq.league_curl as league_curl
import utils.filemap as filemap
import utils.league_util as league_util
import league_conf
import psycopg2
import json

# load_champion_name_id_map Function
# loads the name id map
# that maps the champion name to champion id
# output : a map-like data structure
def load_champion_name_id_map():
    global champion_data
    res = {}
    for id in champion_data:
        name = champion_data[id]['name']
        res[name] = id
        #print(id)
        #print(type(id))
    return res
# data_refresh function
# refreshs the data from riot API
# for champions
def data_refresh():
    cnx = league_util.conn_postgre()
    cursor = cnx.cursor()
    data = league_curl.request('champion')['data']
    res = {}
    for x in data:
        #print(x)
        key = int(data[x]['key'])
        name = data[x]['name']
        #print(key)
        champ_data_str = json.dumps(data[x])
        stmt = 'insert into analytics_champion values(%s,%s,%s)'
        cursor.execute(stmt,[key,name,champ_data_str])
    cnx.commit()

# id_from_champion function
# Top Level Function
# input : champion_name : string
# output : champ_id : int/long
def id_from_champion(name,cursor):
    stmt = 'select champ_id from analytics_champion where LOWER(name) = LOWER(%s)'
    champ_id = None
    try:
        cursor.execute(stmt,[name])
        row = cursor.fetchone()
        if row is not None:
            champ_id = row[0]
    except psycopg2.ProgrammingError:
        champ_id = None
    return champ_id
# data_from_id function
# Top Level Function
# input : champion_id : int
# output : champion data structure from Riot API
def data_from_id(champ_id,cursor):
    stmt = 'select champ_data from analytics_champion where champ_id = %s'
    champ_data = None
    try:
        cursor.execute(stmt,[champ_id])
        row = cursor.fetchone()
        if row is not None:
            champ_data = row[0]
    except psycopg2.ProgrammingError:
        champ_data= None
    return champ_data

# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    pass
def cleanup():
    pass

#testing function
def testing():
    with league_util.conn_postgre() as cnx:
        with cnx.cursor() as cursor:
            assert(id_from_champion('Lux',cursor) == 99)
            assert(id_from_champion('Ahri',cursor) == 103)
            assert(data_from_id(99,cursor)['name'] == 'Lux')

if __name__ == '__main__':
    #data_refresh()
    testing()
