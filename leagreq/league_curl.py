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
static_data_base_url = 'http://ddragon.leagueoflegends.com/cdn/9.23.1/data/en_US'
cj = 'champion.json'
wait_map = {}

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
    res  = {}
    h_p_copy = process_header_map(header_params)
    global request_url_map
    if(is_static_request(r_type)):
        req_str = static_data_base_url + '/' + request_url_map[r_type]
    else:
        req_str = base_url + request_url_map[r_type] + '/' + str(r_value)
        req_str += add_header_query(h_p_copy)
    res['req_str'] = req_str
    res['r_type'] = r_type
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
    return max_wait

def process_app_rate(headers):
    # get_app_rate_limit
    # get_app_rate_count
    # X-App-Rate-Limit
    # X-App-Rate-Limit-Count
    # check if the app-rate-limit is in the header
    if 'X-App-Rate-Limit' not in headers:
        return 0
    app_rate_limits = process_rates(headers['X-App-Rate-Limit'])
    app_rate_counts = process_rates(headers['X-App-Rate-Limit-Count'])
    max_wait = calculate_wait_response(app_rate_limits,app_rate_counts)
    return max_wait
    pass

#
#   Per endpoint keep track of the last time the endpoint was called
#   and the response from the endpoint in order to calculate "have we waited long enough for the method-rate-limit"
#
#
def process_endpoint_rate(headers):

    pass

def add_app_wait_time(wait_time):
    if 'app' not in wait_map:
        wait_map['app'] = {'wait':0, 'time':0}
    wait_map['app']['wait'] = wait_time
    wait_map['app']['time'] = time.time()

# Process response headers which give the rate limits and the current count
# and does the sleep here
#
#
def process_response_headers(headers):
    # Process the application rate limit
    wait_time = process_app_rate(headers)
    if wait_time > 0:
        add_app_wait_time(wait_time)
    #get_endpoint_rate(headers)
    # and also process the endpoint rate limit
    pass
#TODO: What should happen in the event of a 4XX error
# request function
#
# high level function that actually requests the desired resource indicated by r_type and r_value
# with the additional parameters in the header params map
#

def retrieve_app_wait():
    res = 0
    if 'app' in wait_map:
        had_to_wait = wait_map['app']['wait']
        elapsed = time.time() - wait_map['app']['time']
        res = max(had_to_wait - elapsed,0)
    return res


def proper_wait(req):
    app_wait_time = retrieve_app_wait()

    if app_wait_time > 0:
        print("SLEEPING ", app_wait_time,"!!!!!")
        time.sleep(app_wait_time)

def execute_request(req):
    req_str = req['req_str']
    r_type = req['r_type']
    counter = 0
    print(req_str)
    response_json = None
    while counter < 2:
        proper_wait(req)
        response = requests.get(req_str)
        print(response.headers)
        if valid_response(response):
            response_json = response.json()
            counter = 2
        else:
            print(response.text)
            # print(response.headers)
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
    req = gen_request(r_type,r_value,header_params)
    response_json = execute_request(req)
    return response_json



def testing_match_list():
    s1 = request('match_list','PhjloNxjxrIOTQ4trcehe8OGiU9ABj933DBGRnO4GBfqNw',{'season':'4'})
    assert('matches' in s1)
    x = s1['matches']
    for y in x:
        assert('season' in y)
        assert(y['season'] == 4)

def testing_account():
    s1 = request('account','PhjloNxjxrIOTQ4trcehe8OGiU9ABj933DBGRnO4GBfqNw')
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

def multi_wait_test():
    test_subjects = [3218339380,3217748340, 3217743073, 3217030001,3216853512,3216649335,3216644079,3216557548,3215842512,3215807647,3215772284,3215350679,3215146839,
3215114074,3214903763,3214901255,3213701146,3213556389,3213599789,3212815373,3212640620,3211838405,3211844286, 3211830021,3211795291,3211780042,3211704802,3210818094]
    # for x in test_subjects:
    #     request('match',x)
    summoner_names = ['chulchultrain','chulminyang','a2y','jehpoody','crysteenah','sbaneling','summontheez','timbangu','starcalls coffee','blanket robber','ilovememundo',
    'temporaltempest,','gofortheotherguy','kidhybrid','tankage','gosusummoner','black zealot',]
    # for s in summoner_names:
    #     request('summoner',s)
    m_l = request('match_list','PhjloNxjxrIOTQ4trcehe8OGiU9ABj933DBGRnO4GBfqNw')['matches']
    for m in m_l:
        request('match',m['gameId'])
def testing():
    testing_summoner_name_DNE()
    testing_summoner_name_pass()
    testing_account()
    testing_match_list()
    test_timeline()
    test_match()
    multi_wait_test()
    pass

if __name__ == "__main__":
    testing()
    test_static()
