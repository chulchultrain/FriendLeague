import leagreq.league_curl as league_curl
import utils.filemap as filemap
import utils.league_util as league_util
import league_conf

# purpose get champion data like name id all that good shit.
# do i need some sort of associative mapping software in order to do this?
# so that i dont have to have maps from id to name and name to id and all that?
#

champion_data = {}
name_to_id = {}


# load_champion_data_map function
# loads the champion data map
# that maps the champion_id to champion data
# output : a map-like data structure
def load_champion_data_map():
    #return filemap.Filemap(league_conf.champion_data_dir)
    return league_util.load_pickled_map(league_conf.champ_detail_file)


def save_champion_data_map():
    global champion_data
    league_util.save_pickled_map(league_conf.champ_detail_file,champion_data)
    pass

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

def save_champion_name_id_map():
    pass

# data_refresh function
# refreshs the data from riot API
# for champions
def data_refresh():
    global champion_data
    global name_to_id
    data = league_curl.request('champion')['data']
    res = {}
    for x in data:
        #print(x)
        key = int(data[x]['key'])
        #print(key)
        r = data[x]
        champion_data[key] = r
    name_to_id = load_champion_name_id_map()

# id_from_champion function
# Top Level Function
# input : champion_name : string
# output : champ_id : int/long
def id_from_champion(name):
    global champion_data
    global name_to_id
    if name in name_to_id:
        return name_to_id[name]
    else:
        return None

# data_from_id function
# Top Level Function
# input : champion_id : int
# output : champion data structure from Riot API
def data_from_id(id):
    global champion_data
    if id in champion_data:
        return champion_data[id]
    else:
        return None

# setup function
# does all necessary tasks to use this entire module correctly
def setup():
    global champion_data
    global name_to_id
    champion_data = load_champion_data_map()
    name_to_id = load_champion_name_id_map()
    #data_refresh()
def cleanup():
    save_champion_data_map()
    save_champion_name_id_map()

#testing function
def testing():
    assert(id_from_champion('Lux') == 99)
    assert(id_from_champion('Ahri') == 103)
    assert(data_from_id(99)['name'] == 'Lux')
setup()
cleanup()
if __name__ == '__main__':
    testing()
