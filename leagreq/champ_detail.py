import leagreq.league_curl as league_curl
import utils.filemap as filemap
import league_conf

# purpose get champion data like name id all that good shit.
# do i need some sort of associative mapping software in order to do this?
# so that i dont have to have maps from id to name and name to id and all that?
#

champion_data = {}
name_to_id = {}

def load_champion_data_map():
    return filemap.Filemap(league_conf.champion_data_dir)

def save_champion_data_map():
    pass

def load_champion_name_id_map():
    global champion_data
    res = {}
    for id in champion_data:
        name = champion_data[id]['name']
        res[name] = int(id)
    return res

def save_champion_name_id_map():
    pass

def data_refresh():
    global champion_data
    global name_to_id
    data = league_curl.request('champion')['data']
    res = {}
    for x in data:
        key = data[x]['key']
        r = data[x]
        champion_data[key] = r
    name_to_id = load_champion_name_id_map()

def id_from_champion(name):
    global champion_data
    global name_to_id
    if name in name_to_id:
        return name_to_id[name]
    else:
        return None

def data_from_id(id):
    global champion_data
    if id in champion_data:
        return champion_data[id]
    else:
        return None

def setup():
    global champion_data
    global name_to_id
    champion_data = load_champion_data_map()
    name_to_id = load_champion_name_id_map()
    #data_refresh()
def cleanup():
    save_champion_data_map()
    save_champion_name_id_map()
def testing():
    print(id_from_champion('Lux'))
    print(data_from_id(id_from_champion('Ahri')))
    for name in name_to_id:
        print(name + ' ' + str(name_to_id[name]))
setup()
cleanup()
if __name__ == '__main__':
    testing()
