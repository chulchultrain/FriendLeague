import league_conf
import time
import acc_to_matches
import match_detail
import pickle

request_queue = []

def load_request_queue():
    fin = None
    try:
        fin = open(league_conf.request_queue_file,'rb')
        res = pickle.load(fin)
        fin.close()
    except IOError:
        print("Couldn't pickle request queue file")
        res = []
    except EOFError:
        print("Couldn't pickle request queue file")
        res = []
    finally:
        if fin != None:
            fin.close()
    return res

def save_request_queue(request_queue):
    with open(league_conf.request_queue_file,'wb') as fout:
        pickle.dump(request_queue,fout)

def add_to_queue(func,args):
    global request_queue
    request_queue.append([func,args])

def process_one():
    global request_queue
    print(len(request_queue))
    #time.sleep(1)
    if len(request_queue) == 0:
        return False
    req = request_queue[0]
    req_func = req[0]
    req_param = req[1]
    result = req_func(req_param)
    if result is None:
        with open('errfile.txt','a') as fout:
            fout.write(str(req_func) + ' ' + str(req_param) + "failed!\n")
        request_queue.pop(0)
        return False
    else:
        request_queue.pop(0)
        return True

def process_n(n):
    i = 0
    while i < n:
        process_one()
        i += 1

def setup():
    global request_queue
    request_queue = load_request_queue()

def cleanup():
    global request_queue
    save_request_queue(request_queue)

setup()
#testing()
#cleanup()


#For all other scripts
