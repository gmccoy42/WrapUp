from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Stories
from .models import Site
from .models import Keys
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from celery import task
import schedule
from datetime import datetime
import time
import dateutil.parser
from django.utils.timezone import utc
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import tldextract
import os

def index(request):
	if request.method == 'POST':
		try:
			user = authenticate(username=request.POST['userName'], password=request.POST['userPassword'])
			if user is not None:
		    	# the password verified for the user
				if user.is_active:
					auth_login(request, user)
					print("User is valid, active and authenticated")
				else:
					print("The password is valid, but the account has been disabled!")
			else:
			    # the authentication system was unable to verify the username and password
				print("The username and password were incorrect.")
		except Exception:
			print("Post error")	
	if request.user.is_authenticated():
		stories = Stories.objects.filter(user=request.user).all()
		stories = stories.order_by('-rank', '-storyDate')
		paginator = Paginator(stories,20)
		page = request.GET.get('page')
		try:
			stories = paginator.page(page)
		except PageNotAnInteger:
			stories = paginator.page(1)
		except EmptyPage:
			stories = paginator.page(paginator.num_pages)
	else:
		stories = None

	return render(request, 'wrapup/main.html', {'stories': stories})

def site(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			extracted = tldextract.extract(request.POST["newSite"])
			s = Site.objects.create(url=request.POST["newSite"], name="{}.{}".format(extracted.domain, extracted.suffix), user=request.user)
			s.save()
		sites = Site.objects.filter(user=request.user).all()
	else:
		sites = None
	return render(request, 'wrapup/site.html', {'sites':sites})
def key(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			try:
				s = Keys.objects.create(key=request.POST["key"], value=int(request.POST["value"]), user=request.user)
				s.save()
			except:
				print("Blank Value")
		keys = Keys.objects.filter(user=request.user).all()
	else:
		keys = None
	return render(request, 'wrapup/keyword.html', {'keys':keys})

def register(request):
	if request.method == 'POST':
		try:
			u = User.objects.create(username=request.POST["userName"], password=request.POST["userPassword"], email=request.POST["email"])
			s.save()
		except:
			print("Blank Value")
	return render(request, "registration/register.html", {
        'form': form,
    })



