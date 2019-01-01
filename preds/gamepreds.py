import leagreq.match_detail as match_detail
import leagreq.champ_detail as champ_detail
import utils.league_util as league_util

# generates a game condition function that operates on match id
# inputs : game_cond_predicate : the predicate we wish to test
#                              : the predicate should take matcH detail data structure
# output : a game condition function that takes as input a match id and outputs a boolean
# based on whether the condition is true or not
def game_cond(game_cond_predicate):
    #get id. get part id. get team id. check if that team took first drag
    def inner(m,cursor):
        m_d = match_detail.match_data_from_id(m,cursor)
        if m_d is None:
            return False
        return game_cond_predicate(m_d)
    return inner

# if the game is a remake
def is_remake():
    def inner(m_d):
        return m_d['gameDuration'] < 300
    return inner

# whether the game's duration falls within the time interval
def game_len_int_cond(m1,m2):
    def inner(m_d):
        return m_d['gameDuration'] >= m1 and m_d['gameDuration'] <= m2
    return inner

def champ_in_game(champion_name):
    champ_id = champ_detail.id_from_champion(champion_name)
    def inner(m_d):
        participants = m_d['participants']
        for p in participants:
            if p['championId'] == champ_id:
                return True
        return False
    return inner

# see if the enemy team has the champ
#
#
def champ_enemy_team(champion_name,acc_id_li):
    champ_id = champ_detail.id_from_champion(champion_name)
    def inner(m_d):
        #find all players on opposing team
        #check for presence of that champ.
        t_p_map = match_detail.map_team_id_to_part_ids(m_d)
        i = 0
        for a in acc_id_li:
            p_id = match_detail.find_part_id(m_d,a)
            if p_id is not None:
                t_id = match_detail.find_participant_data(m_d,p_id)['teamId']
                break
        for t in t_p_map:
            if t is not t_id:
                for p in t_p_map[t]:
                    p_d = match_detail.find_participant_data(m_d,p)
                    if p_d['championId'] == champ_id:
                        print(m_d['gameId'])
                        return True
        return False
    return inner

def testing():
    #2858500164's actual game len is 1820
    with league_util.conn_postgre() as cnx:
        with cnx.cursor() as cursor:
            is_1820 = game_len_int_cond(1819,1820)
            is_1820_game = game_cond(is_1820)
            assert(is_1820_game(2858500164,cursor))
            isnt_2000 = game_len_int_cond(1821,2000)
            isnt_2000_game = game_cond(isnt_2000)
            assert(not isnt_2000_game(2858500164,cursor))
        cnx.commit()



if __name__ == "__main__":
    testing()
