
from django.shortcuts import render_to_response

def render_unavailable():
    return render_to_response('beanstalk/unavailable.html')

