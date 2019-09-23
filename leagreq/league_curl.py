import requests
import league_conf
import time

# request_url_map_populate function
# Creates a map for sub URLs for queries that may be needed from the Riot API.
# Ex: to get the summoner data from Riot API, you have to add the
# suburl of /lol/summoner/v3/summoners/by-name
# This function is where we put all the necessary queries to the Riot API we
# may need.
def request_url_map_populate():
    request_url_map = {}
    request_url_map['match_list'] = '/lol/match/v4/matchlists/by-account'
    request_url_map['summoner'] = '/lol/summoner/v4/summoners/by-name'
    request_url_map['account'] = '/lol/summoner/v4/summoners/by-account'
    request_url_map['match'] = '/lol/match/v4/matches'
    request_url_map['matchTimeline'] = '/lol/match/v4/timelines/by-match'
    request_url_map['champion'] = 'champion.json'
    return request_url_map


# is_static_request function
# determines whether the request type calls riots static api
# so far only champion data is static
def is_static_request(r_type):
    if r_type is 'champion':
        return True
    else:
        return False

#bunch of globals for use
base_url = 'https://na1.api.riotgames.com'
request_url_map = request_url_map_populate()
static_data_base_url = 'http://ddragon.leagueoflegends.com/cdn/8.19.1/data/en_US'
cj = 'champion.json'

#the way the request url map is set up i can just set it so that champs map to different base url.

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


def gen_request(r_type,r_value=None,header_params=None):
    h_p_copy = process_header_map(header_params)
    global request_url_map
    if(is_static_request(r_type)):
        res = static_data_base_url + '/' + request_url_map[r_type]
    else:
        res = base_url + request_url_map[r_type] + '/' + str(r_value)
    res += add_header_query(h_p_copy)
    return res


def valid_response(response):
    return response.status_code == 200

def split_rates(text):
    return text.split(',')

def calculate_rate(rate_text):
    r_data = rate_text.split(':')
    r_count = int(r_data[0])
    r_time = int(r_data[1])
    return r_count,r_time

def process_rates(text):
    rate_text_li = split_rates(text)
    r_map = {}
    for rate_text in rate_text_li:
        r_count, r_time = calculate_rate(rate_text)
        r_map[r_time] = r_count
    return r_map

def calculate_wait_response(rate_limits,rate_counts):
    max_wait = 0
    for r_time in rate_limits:
        if r_time in rate_counts:
            cur_count = rate_counts[r_time]
            cur_limit = rate_limits[r_time]
            if(cur_count >= cur_limit):
                max_wait = max(max_wait,r_time)
    print("max wait became " + str(max_wait))
    return max_wait

def process_app_rate(headers):
    # get_app_rate_limit
    # get_app_rate_count
    # X-App-Rate-Limit
    # X-App-Rate-Limit-Count
    # check if the app-rate-limit is in the header
    app_rate_limits = process_rates(headers['X-App-Rate-Limit'])
    app_rate_counts = process_rates(headers['X-App-Rate-Limit-Count'])
    max_wait = calculate_wait_response(app_rate_limits,app_rate_counts)
    return max_wait
    pass

def process_endpoint_rate(headers):
    pass

# Process response headers which give the rate limits and the current count
# and does the sleep here
#
#
def process_response_headers(headers):
    # Process the application rate limit
    wait_time = process_app_rate(headers)
    time.sleep(wait_time)
    #get_endpoint_rate(headers)
    # and also process the endpoint rate limit
    pass
#TODO: What should happen in the event of a 4XX error
# request function
#
# high level function that actually requests the desired resource indicated by r_type and r_value
# with the additional parameters in the header params map
#

def execute_request(req_str):
    counter = 0
    print(req_str)
    response_json = None
    while counter < 2:
        response = requests.get(req_str)
        print(response.headers)
        if valid_response(response):
            response_json = response.json()
            counter = 2
        else:
            print(response.text)
        process_response_headers(response.headers) #TODO: IN FUTURE, BECAUSE ENDPOINT HAS DIF RATE LIMIT, MAKE IT HIT DIFFERENTLY FOR THAT ENDPOINT
        counter += 1
    return response_json


# Build in rate limiting
# Once we execute a request,
# We look at the response headers to see if we went over the rate limit.
# If we did, back off for some time in some way depending upon what the headers said
#

# def ex_req(req_str):
#     response = requests.get(req_str)
#     if valid_response(response):
        # proceed as normal

# request
# Top Level function
# requests data from riot api
# r_type : type of request : string
# r_value : value of request : string
# header_params : extra header params in the query : dict
def request(r_type,r_value=None,header_params=None):
    req_str = gen_request(r_type,r_value,header_params)
    response_json = execute_request(req_str)
    return response_json



def testing_match_list():
    s1 = request('match_list','iCu9bp2VLrsnq1cUMqDeE3R1rSgEbZnu99BXT07CpmBx3Q',{'season':'4'})
    assert('matches' in s1)
    x = s1['matches']
    for y in x:
        assert('season' in y)
        assert(y['season'] == 4)

def testing_account():
    s1 = request('account','iCu9bp2VLrsnq1cUMqDeE3R1rSgEbZnu99BXT07CpmBx3Q')
    assert('accountId' in s1)

def test_timeline():
    s1 = request('matchTimeline','2858485810')
    assert('frameInterval' in s1)

def test_match():
    s1 = request('match','2858485810')
    assert('queueId' in s1)

def testing_summoner_name_DNE():
    s1 = request('summoner','timban')
    assert(s1 == None)

def testing_summoner_name_pass():
    s1 = request('summoner','chulchultrain',{'beginTime':'1451628000000','season':'4'})
    assert( 'accountId' in s1)

def test_static():
    res = request('champion')['data']
    assert('Aatrox' in res)

def testing():
    testing_summoner_name_DNE()
    testing_summoner_name_pass()
    testing_account()
    testing_match_list()
    test_timeline()
    test_match()
    pass

if __name__ == "__main__":
    testing()
    test_static()
