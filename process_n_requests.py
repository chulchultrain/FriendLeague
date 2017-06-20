import request_scheduler
import match_detail

import sys

args = sys.argv[1:]
num_to_satisfy = args[0]
n = int(num_to_satisfy)

request_scheduler.process_n(n)

request_scheduler.cleanup()
match_detail.cleanup()
