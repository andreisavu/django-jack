
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

from django.http import Http404
from django.template import RequestContext

from beanstalk.client import Client, CommandFailed
from beanstalk.forms import PutForm

@login_required
def index(request):
    return tube_stats(request)

@login_required
def tube_stats(request, tube=None):
    client = Client()

    if tube is None:
        stats = client.stats().items()
    else:
        try:
            stats = client.stats_tube(tube).items()
        except CommandFailed:
            raise Http404
 
    tubes = client.tubes()

    return render_to_response('beanstalk/index.html', 
        {'stats': stats,
         'tubes': tubes,
         'current_tube': tube
        }, context_instance=RequestContext(request))

@login_required
def put(request):
    if request.method == 'POST':
        form = PutForm(request.POST)
        if form.is_valid():

            client = Client()
            client.use(form.cleaned_data['tube'])

            id = client.put(str(form.cleaned_data['body']), form.cleaned_data['priority'], \
                form.cleaned_data['delay'], form.cleaned_data['ttr'])
 
            request.flash.put(notice='job submited to queue with id #%d' % id)
            return redirect('/beanstalk/put/')
    else:
        form = PutForm()

    return render_to_response('beanstalk/put.html', 
        {'form':form}, context_instance=RequestContext(request))   

