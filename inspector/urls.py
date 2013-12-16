from django.conf.urls import patterns, url

urlpatterns = patterns('inspector',
    url(r'^$', 'views.indexHandler'),
    url(r'status/(?P<status>\d+)', 'views.postStatusHandler'),
)