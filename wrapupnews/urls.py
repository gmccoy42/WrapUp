from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework import routers
from wrapup_api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'rank', views.RankViewSet)
router.register(r'site', views.SiteViewSet)
router.register(r'keys', views.KeysViewSet)
router.register(r'stories', views.StoriesViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('wrapup.urls', namespace="wrapup")),
    url(r'^wrapup/', include('wrapup.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^rest_api/', include('rest_framework.urls', namespace='rest_framework')),
)
