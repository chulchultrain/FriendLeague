import preds.teampreds as teampreds
import preds.playerpreds as playerpreds
import preds.gamepreds as gamepreds

#translate a string that indicates a condition that wants to be tested
#to an actual condition predicate function that can be simply called upon a match id
#input: s : a string that refers to a condition
#output: a condition predicate that can be called on a match id which will return true or false

#Valid Inputs:
# team_first_drag, team_first_tower, team_first_blood, team_win


#TODO: Add player preds because right now only team preds in here
#How can I dynamically add predicates here without the code being incredibly long
#Should that also be within a database or something 

def translate(s):
    if s == 'team_first_drag':
        return teampreds.team_cond(teampreds.first_drag)
    elif s == 'team_first_tower':
        return teampreds.team_cond(teampreds.first_tower)
    elif s == 'team_first_blood':
        return teampreds.team_cond(teampreds.first_blood)
    elif s == 'team_win':
        return teampreds.team_cond(teampreds.team_cond_win)
    else:
        print("DEFAULT FAIL")
