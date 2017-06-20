import acc_to_matches
import match_detail
import request_scheduler
import time

def additional_filter(match,filter_map):
    for x in filter_map:
        if x not in match:
            return False
        else:
            if match[x] != filter_map[x]:
                return False
    return True


def put_matches_into_queue(account_id):
    match_list = acc_to_matches.matches_from_id(account_id)
    filter_map = {'season':8}
    print(match_list[0])
    for x in match_list:
        if additional_filter(x,filter_map):
            request_scheduler.add_to_queue(match_detail.match_data_from_id,x['gameId'])

def new_matches_into_queue(account_id):
    new_match_list = acc_to_matches.new_matches_from_id(account_id)
    if new_match_list is None:
        return
    filter_map = {'season':8}
    for x in new_match_list:
        if additional_filter(x,filter_map):
            request_scheduler.add_to_queue(match_detail.match_data_from_id,x['gameId'])


def put_matches_for_acc_list(li):
    for x in li:
        time.sleep(1)
        put_matches_into_queue(x)


request_scheduler.setup()

do_list = [44649467,
48258111,
38681917,
32139475,
32421132,
36416797,
41057569,
201989747,
461675,
38457291,
47916976,
38566957,
38294348,
218762457]

put_matches_for_acc_list(do_list)

print(len(request_scheduler.request_queue))

request_scheduler.cleanup()
acc_to_matches.cleanup()
