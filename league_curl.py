import requests
import league_conf
#r = requests.get('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/44649467?season=8&champion=41&api_key=RGAPI-304f08eb-8a87-4db6-8445-b05bb2aa6a2c')
#print(r)
#print(r.text)
#y = r.json()
#x = y['matches']
#Wfirst = x[0]
#print(first)

base_url = 'https://na1.api.riotgames.com'
request_url_map = {}

def request_url_map_populate():
    request_url_map = {}
    request_url_map['match_list'] = '/lol/match/v3/matchlists/by-account'
    request_url_map['summoner'] = '/lol/summoner/v3/summoners/by-name'
    request_url_map['match'] = '/lol/match/v3/matches'
    return request_url_map

request_url_map = request_url_map_populate()

def add_header_query(hq_map):
    #TODO
    res = '?'
    headers = []
    for x in hq_map:
        headers.append(x + '=' + hq_map[x])
    header_statement = '&'.join(headers)
    res += header_statement
    return res

def process_header_map(header_params):
    if type(header_params) is not dict:
        h_p_copy = {}
    else:
        h_p_copy = header_params.copy()
    h_p_copy['api_key'] = league_conf.api_key
    return h_p_copy

def gen_request(r_type,r_value,header_params=None):
    h_p_copy = process_header_map(header_params)
    global request_url_map
    res = base_url + request_url_map[r_type] + '/' + str(r_value)
    res += add_header_query(h_p_copy)
    return res


def testing():
    s1 = gen_request('match_list','44649467',{'season':'4'})
    print(s1)
    r1 = requests.get(s1)
    j1 = r1.json()
    ms1 = j1['matches']
    first1 = ms1[0]
    print(first1)
testing()
