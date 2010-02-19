
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

from django.http import Http404
from django.template import RequestContext

from beanstalk.client import Client, CommandFailed, ConnectionError
from beanstalk.forms import PutForm
from beanstalk.shortcuts import render_unavailable

from urlparse import urlsplit

def _multiget(data, keys, default=None):
    ret = {}
    for key in keys:
        ret[key] = data.get(key, default)
    return ret

@login_required
def index(request):
    try:
        client = Client()
    except ConnectionError:
        return render_unavailable()

    stats = _multiget(client.stats(), [
        'current-connections', 
        'uptime', 
        'job-timeouts',
        'version',
        'current-jobs-buried',
        'total-jobs',])

    return render_to_response('beanstalk/index.html', 
        {'stats' : stats},
        context_instance=RequestContext(request))

@login_required
def stats(request):
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

    return render_to_response('beanstalk/stats.html', 
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
def inspect(request, id=None, tube_prefix=''):
    if request.method == 'POST':
        id = request.POST['id']
    
    try:
        id = int(id)
    except (ValueError, TypeError):
        id = None

    try:
        client = Client()
    except ConnectionError:
        return render_unavailable()

    if id:
        job = client.peek(id)
        if job is None:
            request.flash.put(notice='no job found with id #%d' % id)
            stats = []
            buried = False
        else:
            buried = job.stats()['state'] == 'buried'
            stats = job.stats().items()
    else:
        job = None
        stats = []
        buried = False

    tubes = client.tubes()

    return render_to_response('beanstalk/inspect.html',
        {'job': job, 'stats': stats, 'buried': buried, 'tubes': tubes, 'tube_prefix': tube_prefix}, 
        context_instance=RequestContext(request))

def _peek_if(request, status, tube):
    try:
        client = Client()
    except ConnectionError:
        return render_unavailable()

    if not tube: tube = 'default'
    client.use(tube)

    job = getattr(client, "peek_%s" % status)()
    if job is not None:
        return inspect(request, job.jid, tube_prefix='/beanstalk/%s/' % status)

    request.flash.put(notice='no job found')
    return inspect(request, tube_prefix = '/beanstalk/%s/' % status)


@login_required
def ready(request, tube):
    return _peek_if(request, 'ready', tube)


@login_required
def delayed(request, tube):
    return _peek_if(request, 'delayed', tube)

@login_required
def buried(request, tube):
    return _peek_if(request, 'buried', tube)


def _redirect_to_referer_or(request, dest):
    referer = request.META.get('HTTP_REFERER', None)
    if referer is None:
        return redirect(dest)

    try:
        redirect_to = urlsplit(referer, 'http', False)[2]
    except IndexError:
        redirect_to = dest

    return redirect(redirect_to)

@login_required
def job_delete(request, id):
    try:
        client = Client()
        job = client.peek(int(id))

        if job is not None:
            job.delete()
    
        return _redirect_to_referer_or(request, '/beanstalk/inspect/')

    except ConnectionError:
        return render_unavailable()

@login_required
def job_kick(request, id):
    try:
        client = Client()
        client.kick(int(id))

        return redirect('/beanstalk/buried/')

    except ConnectionError:
        return render_unavailable()
    
