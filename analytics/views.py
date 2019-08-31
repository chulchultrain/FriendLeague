from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Account, Champion

def index(request):
    return HttpResponse("Welcome to front page of FriendLeague")

def account(request,name):
    response = "Welcome to account page for %s" % name
    acc = Account.objects.get(name = name)
    context = {
        'account' : acc
    }
    return render(request, 'analytics/account.html',context)

def champion(request,name):
    response = "Welcome to champion page for %s" % name
    champ = Champion.objects.get(name = name)
    context = {
        'champ' : champ
    }
    return render(request, 'analytics/champion.html',context)
