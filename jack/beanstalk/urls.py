from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^stats/$', views.stats),
    (r'^stats_table/$', views.stats_table),
    (r'^put/$', views.put),
    (r'^ready/(?P<tube>[\w-]*)$', views.ready),
    (r'^delayed/(?P<tube>[\w-]*)$', views.delayed),
    (r'^buried/(?P<tube>[\w-]*)$', views.buried),
    (r'^inspect/(?P<id>\d*)$', views.inspect),
    (r'^tube/(?P<tube>[\w-]+)/stats/$', views.tube_stats),
    (r'^job/(?P<id>\d+)/delete/$', views.job_delete),
    (r'^job/(?P<id>\d+)/kick/$', views.job_kick),
)
