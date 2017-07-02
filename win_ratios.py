import match_detail
import acc_to_matches
import name_to_acc

def gen_cmp(x,y):
    if x[1][1] == 0 and y[1][1] == 0:
        return x[1][0] - y[1][0]
    elif x[1][1] == 0:
        return x[1][0]
    elif y[1][1] == 0:
        return y[1][0]
    else:
        xval = float(x[1][0]) / float(x[1][1])
        yval = float(y[1][0]) / float(y[1][1])
        res = xval - yval
        if res > 0:
            return 1
        elif res < 0:
            return -1
        else:
            return 0





#List of friends to a list of summoner names of accounts that they own

def create_friend_subset_id_map(friend_map):
    i = 1
    res = {}
    for x in friend_map:
        res[x] = i
        i *= 2
    return res

def process_match(match,friend_map):
    #TODO:implement
    friend_list = []
    part_id_list = []
    participantIdentities = match['participantIdentities']
    for participant in participantIdentities:
        account_id = participant['player']['accountId']
        for f in friend_map:
            if account_id in friend_map[f]:
                if f not in friend_list:
                    friend_list.append(f)
                    part_id_list.append(participant['participantId'])
    team_id = -1
    participantData = match['participants']
    print(friend_list)
    for p in participantData:
        if p['participantId'] in part_id_list:
            if team_id == -1:
                team_id = p['teamId']
            else:
                if team_id != p['teamId']:
                    print("NOT ON SAME TEAM")
                    return None,None
    if team_id == -1:
        print("COULDNT GET A TEAM")
        return None,None
    team_data = match['teams']
    for t in team_data:
        if t['teamId'] == team_id:
            if t['win'] == 'Win':
                return friend_list,True
            else:
                return friend_list,False
    print("NEITHER TEAM EXISTED")
    return None,None

def friend_list_to_subset_id(friend_subset_id_map,friends_in_game):
    #TODO: implement
    res = 0
    for x in friends_in_game:
        res |= friend_subset_id_map[x]
    return res
    pass

def update_win_ratio(subset_id_to_win_ratio,subset_id,won):
    #TODO: implement
    if subset_id not in subset_id_to_win_ratio:
        subset_id_to_win_ratio[subset_id] = [0,0]
    if won:
        subset_id_to_win_ratio[subset_id][0] += 1
    else:
        subset_id_to_win_ratio[subset_id][1] += 1

def subset_id_to_friend_list(friend_to_subset_id_map,subset_id):
    #TODO: implement
    res = []
    for f in friend_to_subset_id_map:
        if subset_id & friend_to_subset_id_map[f]:
            res.append(f)
    return res

def translate_summoner_to_acc_id_map(friend_map):
    res = {}
    for f in friend_map:
        res[f] = []
        for x in friend_map[f]:
            res[f].append(name_to_acc.account_id_from_name(x))
    return res

def win_ratios(friend_map,match_list):
    #Keep a win_ratio of friend_list subsets to a win_ratio(win/loss #'s)
    #
    #make a friend to subset_id map
    #for each game, find its subset id.
    #make sure the game is valid. such as all friends were on the same team.
    # for same game, find whether they won or not.
    # update subset_id to win_ratio map
    acc_map = translate_summoner_to_acc_id_map(friend_map)
    subset_id_to_win_ratio = {}
    friend_to_subset_id_map = create_friend_subset_id_map(acc_map)
    for m in match_list:
       friends_in_game,won = process_match(m,acc_map) #TODO:implement
       subset_id = friend_list_to_subset_id(friend_to_subset_id_map,friends_in_game) #TODO:implement
       update_win_ratio(subset_id_to_win_ratio,subset_id,won) #TODO:implement

    res = []
    for x in subset_id_to_win_ratio:
        fl = subset_id_to_friend_list(friend_to_subset_id_map,x) #TODO:implement
        current_win_ratio = subset_id_to_win_ratio[x]
        res.append([fl,current_win_ratio])
    return res

def testing():
    f_m = {}
    f_m['Thomas'] = ['chulminyang','chulchultrain']
    f_m['Christina'] = ['crysteenah']
    f_m['Joon'] = ['Gosusummoner','Black Zealot']
    f_m['Tim'] = ['Starcalls Coffee', 'Timbangu']
    f_m['Johnny'] = ['mikiilolirl','TSM Taha']
    f_m['Khai'] = ['King Doran','Krazen']
    f_m['Jae'] = ['summontheez']
    f_m['Tan'] = ['fearbreeder','Datevape']
    match_list = []
    for x in match_detail.match_id_to_data:
        match_list.append(match_detail.match_id_to_data[x])
    res = win_ratios(f_m,match_list)
    for x in res:
        print(x)
testing()
