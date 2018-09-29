import leagreq.match_detail as match_detail

# generates a game condition function that operates on match id
# inputs : game_cond_predicate : the predicate we wish to test
#                              : the predicate should take matcH detail data structure
# output : a game condition function that takes as input a match id and outputs a boolean
# based on whether the condition is true or not
def game_cond(game_cond_predicate):
    #get id. get part id. get team id. check if that team took first drag
    def inner(m):
        m_d = match_detail.match_data_from_id(m)
        if m_d is None:
            return False
        return game_cond_predicate(m_d)
    return inner

# if the game is a remake
def is_remake(m_d):
    return m_d['gameDuration'] < 300

# whether the game's duration falls within the time interval
def game_len_int_cond(m1,m2):
    def inner(m_d):
        return m_d['gameDuration'] >= m1 and m_d['gameDuration'] <= m2
    return inner


def testing():
    #2858500164's actual game len is 1820
    is_1820 = game_len_int_cond(1819,1820)
    is_1820_game = game_cond(is_1820)
    assert(is_1820_game(2858500164))
    isnt_2000 = game_len_int_cond(1821,2000)
    isnt_2000_game = game_cond(isnt_2000)
    assert(not isnt_2000_game(2858500164))
    pass


if __name__ == "__main__":
    testing()
