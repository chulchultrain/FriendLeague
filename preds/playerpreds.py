import leagreq.match_detail as match_detail
import leagreq.match_timeline as match_timeline
import leagreq.champ_detail as champ_detail

# generates a player condition function that operates on a match id
# inputs: id - account id of the player in question
#         player_cond_predicate - the predicate we wish to test
#                               - the predicate should take the participant_data as an input
# output: a player condition function that takes a match id as input and returns a boolean based on whether the condition is true or not
def player_cond(id,player_cond_predicate):
    def inner(m_id):
        m_d = match_detail.match_data_from_id(m_id)
        if m_d is None:
            return False
        in_map = match_detail.inter_map(m_d)
        part_data = match_detail.id_to_data(in_map,id,id_type='account_id',result_type='part_data')
        if part_data is None:
            return False
        return player_cond_predicate(part_data)
    return inner

#def player_list_cond(id_li,player_cond_predicate):
#    def inner(m_id):
#        m_d = match_detail.match_d`ata_from_id(m_id)
#        if m_d is None:
#            return False
#        res = True
#        for id in id_li:
#            part_data = match_detail.player_data_from_match(m_d,id)
#            if part_data is None:


# a player predicate generator that takes in a champion name as input and outputs a predicate function that operates on player data
# tests whether a certain champ is played
# input: champ_name - the name of the champion to be tested
# output: a predicate function that tests whether the player was playing that champ
def plays_champ(champ_name):
    id = champ_detail.id_from_champion(champ_name)
    def inner(p_d):
        return p_d['championId'] == id
    return inner

# accessory function for the is_lane function. calculates what lane is being played
def calculate_lane(p_d):
    lane = p_d['timeline']['lane']
    if lane == 'MID':
        lane = 'MIDDLE'
    if lane == 'BOT':
        lane = 'BOTTOM'
    return lane

# a player predicate generator that takes in a lane as input and outputs a predicate function that operates on player data
# tests whether a certain lane is played
# input: lane - the lane to be tested
# output: a predicate function that tests whether the player was playing that lane
def is_lane(lane):
    def inner(p_d):
        return calculate_lane(p_d) == lane
    return inner

def got_first_blood():
    def inner(p_d):
        #if p_d is None:
        #    print("PARTICIPANT DATA IS NONE")
        if 'firstBloodKill' in p_d['stats']:
            return p_d['stats']['firstBloodKill']
        else:
            return False
    return inner

def testing():
    is_top = is_lane('TOP')
    i_am_top = player_cond(38566957,is_top)
    assert(i_am_top(2858500164))
    is_mid = is_lane('MIDDLE')
    i_am_mid = player_cond(38566957,is_mid)
    assert(i_am_mid(2858500164) == False)
    is_camille = plays_champ('Camille')
    i_am_camille = player_cond(38566957,is_camille)
    assert(i_am_camille(2858500164))
    christina_is_camille = player_cond(48258111,is_camille)
    assert(christina_is_camille(2858500164) == False)
if __name__ == "__main__":
    testing()
