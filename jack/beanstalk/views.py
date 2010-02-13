
from django.shortcuts import render_to_response, redirect

def index(request):
    return render_to_response('beanstalk/index.html')

