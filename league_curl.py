import requests
import league_conf
#import league_exceptions
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
        headers.append(x + '=' + str(hq_map[x]))
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

def check_json(json_obj):
    if 'status' in json_obj:
        raise RuntimeError("Response JSON improperly formatted")


#TODO: What should happen in the event of a 4XX error
def request(r_type,r_value,header_params=None):
    req_str = gen_request(r_type,r_value,header_params)
    print(req_str)
    response = requests.get(req_str)
    response_json = response.json()
    #print(type(response_json))
    #print(response_json)
    #for keys in response_json:
    #    print(keys + ' ' + str(response_json[keys]))
    try:
        check_json(response_json)
    except RuntimeError as e:
        print(e)
        response_json = None

    return response_json



def testing_match_list():
    s1 = request('match_list','44649467',{'season':'4'})
    if 'matches' in s1:
        x = s1['matches']
        for y in x:
            if 'season' in y:
                if y['season'] != 4:
                    print("Didn't filter season properly")
                    print(y['season'])
            else:
                print("Season not in a match record")
    else:
        print("NOT WORKING AS INTENDED")


    #if s1 == None:
    #    print("GOOD AS INTENDED TO FAIL")
    #else:
    #    print("FAIL TEST NOT WORKING AS INTENDED")


def testing_summoner_name_DNE():
    s1 = request('summoner','timban')

    if s1 == None:
        print("GOOD AS INTENDED TO FAIL")
    else:
        print("DNE TEST NOT WORKING AS INTENDED")

def testing_summoner_name_pass():
    s1 = request('summoner','chulchultrain',{'beginTime':'1451628000000','season':'4'})
    if 'accountId' in s1:
        print("GOOD PASSED AS INTENDED")
        print(s1)
    else:
        print("EXISTING NAME TEST NOT WORKING AS INTENDED")

def testing():
    testing_summoner_name_DNE()
    #testing_summoner_name_pass()
    #testing_match_list()
testing()
