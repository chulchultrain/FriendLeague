import leagreq.match_detail as match_detail
import utils.league_util as league_util
#import leagreq.match_timeline as match_timeline



# generates a team condition function that operates on a match id
# inputs : acc_id_li : list of account ids of players that could be on the team
#          team_cond_predicate : the predicate we wish to test
#                              : the predicate function should take teamdata as an input
# output : a team condition function that takes a match id as input and returns a boolean
# based on whether the condition is true or not
def team_cond(team_cond_predicate):
    #get id. get part id. get team id. check if that team took first drag
    def intermediate(acc_id_li):
        def inner(m,cursor):
            m_d = match_detail.match_data_from_id(m,cursor)
            if m_d is None:
                return False
            in_map = match_detail.inter_map(m_d)
            for a in acc_id_li:
                t_d = match_detail.id_to_data(in_map,a,id_type='account_id',result_type='team_data')
                if t_d is not None:
                    break

            return team_cond_predicate(t_d)
        return inner
    return intermediate
#def iterate_team_players_cond(acc_id_li,team_cond_predicate):


#predicates below should be self-explanatory

#def iterate_part_team_cond(acc_id_li,player_cond_predicate,how_to_aggregate):
#    def inner(m):
#        find_part_id =

def other_team_cond(teamid):
    pass
def iterate_part_team_cond(teamid,player_cond_predicate):
    def inner(m):
        m_d = match_detail.match_data_from_id(m)
        if m_d is None:
            return False
        part_list = m_d['participants']
        res = True
        for p in part_list:
            if p['teamId'] == teamid:
                res = res and player_cond_predicate(p)
        return res
    return inner
    # for each participant in the team, find wehter its true for all of them
# predicate for whether the team won

def team_cond_win(td):
    return td['win'] == 'Win'

# predicate for first dragon taken
def first_drag(td):
    return td['firstDragon']

# predicate for first tower
def first_tower(td):
    return td['firstTower']

# predicate for first blood
def first_blood(td):
    return td['firstBlood']

# predicate for first drag and tower
def first_drag_and_tower(td):
    return first_drag(td) and first_tower(td)

# predicate for first drag or first tower
def first_drag_or_tower(td):
    return first_drag(td) or first_tower(td)

# predicate for first baron
def first_baron(td):
    return td['firstBaron']

# predicate for first rift herald
def first_rift(td):
    return td['firstRiftHerald']

# predicate for first drag first tower and win game
def first_drag_tower_and_win(td):
    return first_drag_and_tower(td) and team_cond_win(td)

# predicate for not getting first tower
def miss_first_tower(td):
    return td['firstTower'] is False

# predicate for not getting first dragon
def miss_first_drag(td):
    return td['firstDragon'] is False

# predicate for not getting first dragon and not getting first tower
def miss_first_drag_and_tower(td):
    return first_drag_or_tower(td) is False

def testing():
    with league_util.conn_postgre() as cnx:
        with cnx.cursor() as cursor:
            acc_id_li = [38566957,48258111,32139475,33226921]
            gfd = team_cond(first_drag)(acc_id_li)
            gfb = team_cond(first_blood)(acc_id_li)
            won = team_cond(team_cond_win)(acc_id_li)
            assert(gfd(2875873602,cursor))
            assert(gfb(2875873602,cursor))
            assert(not won(2875873602,cursor) )
        cnx.commit()

if __name__ == "__main__":
    testing()
