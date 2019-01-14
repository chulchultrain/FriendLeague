from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from .models import Account
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.

def index(request):
    return HttpResponse("Hello, World. analytics index")

def account(request,name):
    # Recent X games, print some stats about them, like the
    #
    #
    #TODO: if name doesnt exist then retrieve from riot API and recreate
    acc = get_object_or_404(Account,name=name)
    params = {'account': acc}
    return render(request,'analytics/account.html',params)
    #return HttpResponse("Hello, World. " + acc.account_id)
