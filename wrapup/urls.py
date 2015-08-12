from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^site/$', views.site, name='site'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^register/$', views.register, name='register'),
    url(r'^key/$', views.key, name='key'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
   
]