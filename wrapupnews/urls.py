from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('wrapup.urls', namespace="wrapup")),
    url(r'^wrapup/', include('wrapup.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
