from django.conf.urls import patterns, url

urlpatterns = patterns('poster',
    url(r'delete', 'views.deleteHandler'),
    url(r'$', 'views.postHandler'),
)