
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

from django.http import Http404
from django.template import RequestContext

from beanstalk.client import Client, CommandFailed, ConnectionError
from beanstalk.forms import PutForm
from beanstalk.shortcuts import render_unavailable

@login_required
def index(request):
    return tube_stats(request)

@login_required
def tube_stats(request, tube=None):
    try:
        client = Client()
    except ConnectionError:
        return render_unavailable()

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

            try:
                client = Client()
            except ConnectionError:
                return render_unavailable()

            client.use(form.cleaned_data['tube'])

            id = client.put(str(form.cleaned_data['body']), form.cleaned_data['priority'], \
                form.cleaned_data['delay'], form.cleaned_data['ttr'])
 
            request.flash.put(notice='job submited to queue with id #%d' % id)
            return redirect('/beanstalk/put/')
    else:
        form = PutForm()

    return render_to_response('beanstalk/put.html', 
        {'form':form}, context_instance=RequestContext(request))   

@login_required
def inspect(request, id=None):
    if request.method == 'POST':
        id = request.POST['id']
    
    try:
        id = int(id)
    except (ValueError, TypeError):
        id = None

    if id:
        try:
            client = Client()
        except ConnectionError:
            return render_unavailable()

        job = client.peek(id)
        if job is None:
            request.flash.put(notice='no job found with id #%d' % id)
            stats = []
        else:
            stats = job.stats().items()
    else:
        job = None
        stats = []

    return render_to_response('beanstalk/inspect.html',
        {'job':job, 'stats':stats}, context_instance=RequestContext(request))

def _peek_if(request, status):
    try:
        client = Client()
    except ConnectionError:
        return render_unavailable()

    job = getattr(client, "peek_%s" % status)()
    if job is not None:
        return inspect(request, job.jid)

    request.flash.put(notice='no job found')
    return redirect('/beanstalk/inspect/')


@login_required
def ready(request):
    return _peek_if(request, 'ready')


@login_required
def delayed(request):
    return _peek_if(request, 'delayed')

@login_required
def buried(request):
    return _peek_if(request, 'buried')

