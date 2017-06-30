import requests
import league_conf
import time




# request_url_map_populate function
# Creates a map for sub URLs for queries that may be needed from the Riot API.
# Ex: to get the summoner data from Riot API, you have to add the
# suburl of /lol/summoner/v3/summoners/by-name
# This function is where we put all the necessary queries to the Riot API we
# may need.
#
#
def request_url_map_populate():
    request_url_map = {}
    request_url_map['match_list'] = '/lol/match/v3/matchlists/by-account'
    request_url_map['summoner'] = '/lol/summoner/v3/summoners/by-name'
    request_url_map['match'] = '/lol/match/v3/matches'
    return request_url_map

base_url = 'https://na1.api.riotgames.com'
request_url_map = request_url_map_populate()

# add_header_query function
# Creates the substring to be added to the end of a Riot API request URL for
# parameters that we need passed to the query, such as API_KEY
# (our authentication) and beginTime for filtering the actual query results
# before it reaches us.
#
def add_header_query(hq_map):
    #TODO
    res = '?'
    headers = []
    for x in hq_map:
        headers.append(str(x) + '=' + str(hq_map[x]))
    header_statement = '&'.join(headers)
    res += header_statement
    return res

# process_header_map function
# This function is a preprocessing function to be used on a header before it is
# passed into the add_header_query function. First, it performs a type check
# to make sure that the map is indeed a map. Then it adds the API key because
# you will always need the API key in order to make a request upon Riot API.

def process_header_map(header_params):
    if type(header_params) is not dict:
        h_p_copy = {}
    else:
        h_p_copy = header_params.copy()
    h_p_copy['api_key'] = league_conf.api_key
    return h_p_copy

# gen_request
# function to create the actual string that represents the request URL
# for the requested resources indicated by r_type and r_value
# with the additional parameters in the header_params map


def gen_request(r_type,r_value,header_params=None):
    h_p_copy = process_header_map(header_params)
    global request_url_map
    res = base_url + request_url_map[r_type] + '/' + str(r_value)
    res += add_header_query(h_p_copy)
    return res

# check_json
# checks to see if something was actually returned
# as of 20170626, its not a very thorough check. perhaps should be updated.

def check_json(json_obj):
    if 'status' in json_obj:
        raise RuntimeError(str(json_obj))


#TODO: What should happen in the event of a 4XX error
# request function
#
# high level function that actually requests the desired resource indicated by r_type and r_value
# with the additional parameters in the header params map
#
def request(r_type,r_value,header_params=None):
    time.sleep(1)
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

    else:
        print("EXISTING NAME TEST NOT WORKING AS INTENDED")

def testing():
    testing_summoner_name_DNE()
    testing_summoner_name_pass()
    testing_match_list()
#testing()
