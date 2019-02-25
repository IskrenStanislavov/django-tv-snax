from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('users.urls')),
    url(r'', include('prizes.urls')),
    url(r'', include('programs.urls')),
    url(r'', include('recognition.urls')),
)
