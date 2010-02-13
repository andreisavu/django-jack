from django.conf.urls.defaults import *
from django.shortcuts import redirect
from abspath import abspath

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', lambda req:redirect('/beanstalk/')),
    (r'^beanstalk/', include('beanstalk.urls')),

    (r'^accounts/login/$', 'django.contrib.auth.views.login', 
        {'template_name':'accounts/login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': abspath('media')}),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
