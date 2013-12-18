from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'JobCrawler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^crawler', include('crawler.urls')),
    url(r'^poster', include('poster.urls')),
    url(r'^inspector', include('inspector.urls')),
)

urlpatterns += staticfiles_urlpatterns()