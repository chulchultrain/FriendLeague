
def plays_champ(champ_name):
    id = champ_detail.id_from_champion(champ_name)
    def inner(match_general):
        return match_general['champion'] == id
    return inner


def is_win(name):
    acc_id = name_to_acc.account_id_from_name(name)
    def inner(m_d):
        part_id = match_detail.find_part_id(m_d,acc_id)
        t_d = match_detail.team_data(m_d,part_id)
        return t_d['win'] == 'Win'
    return inner

def calculate_lane(match_general):
    lane = match_general['lane']
    if lane == 'MID':
        lane = 'MIDDLE'
    if lane == 'BOT':
        lane = 'BOTTOM'
    return lane

def is_lane(lane):
    def inner(match_general):
        return calculate_lane(match_general) == lane
    return inner
