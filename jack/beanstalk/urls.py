from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^put/$', views.put),
    (r'^inspect/(?P<id>\d*)$', views.inspect),
    (r'^tube/(?P<tube>\w+)/stats/$', views.tube_stats),
)
