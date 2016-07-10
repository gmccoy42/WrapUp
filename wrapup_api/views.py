from django.shortcuts import render
from django.contrib.auth.models import User
from wrapup.models import Keys, Site, Stories, Rank
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .serializer import UserSerializer, KeysSerializer, SiteSerializer, StoriesSerializer, RankSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class KeysViewSet(viewsets.ModelViewSet):
    queryset = Keys.objects.all()
    serializer_class = KeysSerializer

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class StoriesViewSet(viewsets.ModelViewSet):
    queryset = Stories.objects.all()
    serializer_class = StoriesSerializer

class RankViewSet(viewsets.ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer

