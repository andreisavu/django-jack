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
)
