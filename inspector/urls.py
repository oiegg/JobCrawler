from django.conf.urls import patterns, url

urlpatterns = patterns('inspector',
    url(r'^$', 'views.indexHandler'),
    url(r'login', 'views.loginHandler'),
    url(r'admin', 'views.adminHandler'),
    url(r'status/(?P<status>\d+)', 'views.postStatusHandler'),
    # url(r'info', 'views.infoFilterHandler'),
)