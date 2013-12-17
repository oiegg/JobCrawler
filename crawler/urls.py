from django.conf.urls import patterns, url

urlpatterns = patterns('crawler',
    url(r'add/(?P<cid>\d+)', 'views.addHandler'),
    url(r'add$', 'views.addHandler'),
    url(r'update', 'views.updateHandler'),
)