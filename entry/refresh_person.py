# Module to serve as a runnable script to refresh a persons matchlist and data in the db.
# python3 -m entry.refresh_person.py
# Command line arguments:
# --name
# --acc_id encrypted account id using the api key
# Will retrieve the updated match list from the api,
# and for matches that are not in the db, it will populate them in the db
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'FriendLeague.settings'
import sys
import argparse
import django
from django.conf import settings
if __name__ == '__main__':
    django.setup()


def refresh_person(acc_id):
    # refresh match list
    # for all matches not in db, put them in

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-n',"--name",help = "the name of the summoner")
    parser.add_argument('-a',"--acc_id",help = "the account id of the summoner properly encrypted using the api key")
    args = parser.parse_args()
    return args.name, args.acc_id


if __name__ == "__main__":
    name, acc_id = parse_args(sys.argv)
