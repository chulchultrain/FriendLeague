import leagreq.match_detail as match_detail

def game_cond(game_cond_predicate):
    #get id. get part id. get team id. check if that team took first drag
    def inner(m):
        m_d = match_detail.match_data_from_id(m)
        if m_d is None:
            return False
        return game_cond_predicate(m_d)
    return inner

def is_remake(m_d):
    return m_d['gameDuration'] < 300

def game_len_int_cond(m1,m2):
    def inner(m_d):
        return m_d['gameDuration'] >= m1 and m_d['gameDuration'] <= m2
    return inner
