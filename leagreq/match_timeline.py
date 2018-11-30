import leagreq.league_curl as league_curl
import league_conf
import utils.league_util as league_util
import utils.sqlitemap as sqlitemap

match_id_to_timeline_map = {}


# load_match_timeline_map function
# returns the map like data structure that maps match id
# to match timeline data structure
def load_match_timeline_map():
    res = sqlitemap.SqliteMap(league_conf.match_timeline_db)
    return res

# save_match_timeline_map function
# saves the map like data structure that maps match id
# to match timeline data structure
def save_match_timeline_map():
    pass


# match_timeline_refresh_function
# calls the Riot API to retrieve match timeline data for a specific match id
# input : match id : int
# output : match timeline data structure
def match_timeline_refresh(match_id):
    match_timeline = league_curl.request('matchTimeline',match_id)
    if match_timeline is None:
        print("COULDN'T FIND MATCH TIMELINE " + str(match_id))
    return match_timeline
    pass
# match_timeline_from_id function
# Top level function
# returns match line data from a specific match id
def match_timeline_from_id(match_id):
    global match_id_to_timeline_map
    if match_id not in match_id_to_timeline_map:
        match_id_to_timeline_map[match_id] = match_timeline_refresh(match_id)
    return match_id_to_timeline_map[match_id]

def setup():
    global match_id_to_timeline_map
    match_id_to_timelime_map = load_match_timeline_map()

def cleanup():
    save_match_timeline_map()

def testing():
    mt = match_timeline_from_id(2858485810)
    events3 = mt['frames'][3]['events']
    #print(events3)
    assert(events3[-6]['type'] == 'CHAMPION_KILL')

    pass
setup()
if __name__ == '__main__':
    testing()

cleanup()
