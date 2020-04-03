from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,get_object_or_404
from .models import Account, Champion, Match_Detail, Match_Summary
from .view_helpers import filter_match
def index(request):
    return HttpResponse("Welcome to front page of FriendLeague")

def account(request,name):
    # way the tables are currently set up. i'll have to do some processing on this side in order to display
    # the proper values without template overload.

    response = "Welcome to account page for %s" % name
    acc = get_object_or_404(Account,name = name)
    recent_matches = acc.flex_match_list[-5:] #TODO: not just flex but solo also
    match_summary_map = {}
    match_summary_list = Match_Summary.objects.filter(pk__in=recent_matches)
    for m in match_summary_list:
        match_summary_map[m.match_id] = m.match_summary


    context = {
        'account' : acc ,
        'recent_5': recent_matches,
        'match_summary_list': match_summary_map
    }
    return render(request, 'analytics/account.html',context)

def champion(request,name):
    response = "Welcome to champion page for %s" % name
    champ = Champion.objects.get(name = name)
    context = {
        'champ' : champ
    }
    return render(request, 'analytics/champion.html',context)
