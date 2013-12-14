from django.conf.urls import patterns, url

urlpatterns = patterns('crawler',
    url(r'add', 'views.addHandler'),
    url(r'update', 'views.updateHandler'),
)