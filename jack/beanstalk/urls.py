from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^put/$', views.put),
    (r'^ready/$', views.ready),
    (r'^delayed/$', views.delayed),
    (r'^buried/$', views.buried),
    (r'^inspect/(?P<id>\d*)$', views.inspect),
    (r'^tube/(?P<tube>\w+)/stats/$', views.tube_stats),
    (r'^job/(?P<id>\d+)/delete/$', views.job_delete),
    (r'^job/(?P<id>\d+)/kick/$', views.job_kick),
)
