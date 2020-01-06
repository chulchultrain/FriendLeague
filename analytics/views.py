from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Account, Champion

def index(request):
    return HttpResponse("Welcome to front page of FriendLeague")

def account(request,name):
    response = "Welcome to account page for %s" % name
    acc = Account.objects.get(name = name)
    recent_matches = acc.flex_match_list[:-5] #TODO: not just flex but solo also
    context = {
        'account' : acc , 
        'recent_5': recent_matches
    }
    return render(request, 'analytics/account.html',context)

def champion(request,name):
    response = "Welcome to champion page for %s" % name
    champ = Champion.objects.get(name = name)
    context = {
        'champ' : champ
    }
    return render(request, 'analytics/champion.html',context)
