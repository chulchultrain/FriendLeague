import leagreq.match_detail as match_detail
#import leagreq.match_timeline as match_timeline




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


def team_cond_win(td):
    return td['win'] == 'Win'

def first_drag(td):
    return td['firstDragon']

def miss_first_tower(td):
    return td['firstTower'] is False

def miss_first_drag(td):
    return td['firstDragon'] is False

def first_tower(td):
    return td['firstTower']

def first_blood(td):
    return td['firstBlood']

def first_drag_and_tower(td):
    return first_drag(td) and first_tower(td)

def first_drag_or_tower(td):
    return first_drag(td) or first_tower(td)

def first_drag_tower_and_win(td):
    return first_drag_and_tower(td) and team_cond_win(td)

def miss_first_drag_and_tower(td):
    return first_drag_or_tower(td) is False
