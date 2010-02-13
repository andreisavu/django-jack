
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

from beanstalk.client import Client

@login_required
def index(request):
    return tube_stats(request)

@login_required
def tube_stats(request, tube=None):
    client = Client()

    if tube is None:
        stats = client.stats().items()
    else:
        stats = client.stats_tube(tube).items()
    tubes = client.tubes()

    return render_to_response('beanstalk/index.html', 
        {'stats': stats,
         'tubes': tubes,
         'current_tube': tube
        })


