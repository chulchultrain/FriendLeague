import leagreq.match_detail as match_detail
#import leagreq.match_timeline as match_timeline



# generates a team condition function that operates on a match id
# inputs : acc_id_li : list of account ids of players that could be on the team
#          team_cond_predicate : the predicate we wish to test
#                              : the predicate function should take teamdata as an input
# output : a team condition function that takes a match id as input and returns a boolean
# based on whether the condition is true or not
def team_cond(acc_id_li,team_cond_predicate):
    #get id. get part id. get team id. check if that team took first drag

    def inner(m):
        m_d = match_detail.match_data_from_id(m)
        if m_d is None:
            return False
        for a in acc_id_li:
            part_id = match_detail.find_part_id(m_d,a) #can optimize for inner loop repetition later
            if part_id is not None:
                break
        #part_id = match_detail.find_part_id(m_d,acc_id)
        t_d = match_detail.team_data(m_d,part_id)
        return team_cond_predicate(t_d)
    return inner

#predicates below should be self-explanatory

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
    acc_id_li = [38566957,48258111,32139475,33226921]
    gfd = team_cond(acc_id_li,first_drag)
    gfb = team_cond(acc_id_li,first_blood)
    won = team_cond(acc_id_li,team_cond_win)
    assert(gfd(2875873602))
    assert(gfb(2875873602))
    assert(not won(2875873602) )

if __name__ == "__main__":
    testing()