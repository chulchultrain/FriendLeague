import leagreq.league_curl as league_curl
import leagreq.match_detail as match_detail
import leagreq.acc_to_matches as acc_to_matches
import leagreq.name_to_acc as name_to_acc
import leagreq.match_detail as match_detail
import leagreq.champ_detail as champ_detail
def is_remake(match):
    return match['gameDuration'] < 240

def is_wanted_game(match,filter_func):
    filter_func(match)

def playschamp(match_general,champion_name):
    champ_id = champ_detail.id_from_champion(champion_name)
    print(champ_id)
    print(match_general['champion'])
    if champ_id == match_general['champion']:
        print("YES")
    else:
        print("NO")
    return match_general['champion'] == champ_id


def find_part_id(match,id):
    part_id_li = match['participantIdentities']
    for p in part_id_li:
        if p['player']['accountId'] == id:
            return p['participantId']
    return None

def find_team_id(match,participantId):
    parts = match['participants']
    for p in parts:
        if p['participantId'] == participantId:
            res = p['teamId']
    #print("The Team ID is " + res)
    return res

def teamMatchWin(match,teamId):
    teamData = match['teams']
    for t in teamData:
        #print(t['teamId'])
        if t['teamId'] == teamId:
            res = t['win'] == 'Win'
    return res

def is_win(match,id):
    #find the participant id. find which team the player was on
    part_id = find_part_id(match,id)
    team_id = find_team_id(match,part_id)
    win = teamMatchWin(match,team_id)
    return win


def solo_win_rate_for_id(id):
    matches = acc_to_matches.solo_q_matches(id)
    win,loss = 0,0
    for matchgen in matches:
        match_id = matchgen['gameId']
        m = match_detail.match_data_from_id(match_id)
        if is_remake(m) is False:
            if is_win(m,id):
                win += 1
            else:
                loss += 1
        #get the match data and find out whether it was a win
    total = win + loss
    print("wins are " + str(win))
    print("losses are " + str(loss))
    return win * 1.0 / total * 1.0

def win_rate_for_champion(name,champion_name):
    id = name_to_acc.account_id_from_name(name)
    matches = acc_to_matches.matches_from_id(id)
    print("whoop ")
    win,loss = 0,0
    print(len(matches))
    for matchgen in matches:
        match_id = matchgen['gameId']
        if playschamp(matchgen,champion_name) is False:
            continue
        m = match_detail.match_data_from_id(match_id)
        if is_win(m,id):
            win += 1
        else:
            loss += 1
    total = win + loss
    print(win)
    print(loss)
    return win * 1.0 / total * 1.0

def solo_win_rate(name):
    id = name_to_acc.account_id_from_name(name)
    return solo_win_rate_for_id(id)

def setup():
    pass

def cleanup():
    acc_to_matches.cleanup()
    match_detail.cleanup()
    pass

def test_is_win():
    game_ids = [2872527555, 2872517083,2872383477]
    expected = [False,False,True]
    matches = list(map(match_detail.match_data_from_id,game_ids))
    for i,m in enumerate(matches):
        if expected[i] != is_win(m,38566957):
            print("UNEXPECTED MISMATCH " + str(i))
def testing():
    #print(solo_win_rate('chulminyang'))
    #print(solo_win_rate('crysteenah'))
    print(win_rate_for_champion('crysteenah','Lux'))
setup()
if __name__ == '__main__':
    test_is_win()
    #testing()
cleanup()
