


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
    return td['firstDragon'] and td['firstTower']
