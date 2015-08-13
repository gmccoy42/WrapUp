from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Stories
from .models import Site
from .models import Keys
from .models import Rank
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from celery import task
import schedule
from datetime import datetime
import time
import dateutil.parser
from django.utils.timezone import utc
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import tldextract
import os
import commands

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
				messages.error(request, "The username and password were incorrect.")
		except Exception:
			print("Post error")	
	if request.user.is_authenticated():
		ranks = Rank.objects.filter(user=request.user).all()
		ranks = ranks.order_by('-value')

		stories = []
		for rank in ranks:
			stories.append({'story':rank.story, 'rank':rank.value})

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

	return render(request, 'wrapup/main.html', {'stories': stories })

def site(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			extracted = tldextract.extract(request.POST["newSite"])
			try:
				exists = Site.objects.get(url=request.POST["newSite"])
				try:
					exists.user.add(request.user)
					stories = Stories.objects.filter(site=exists.name).all()
					for story in stories:
						story.user.add(request.user)
						r = Rank.objects.create(value=0, user=request.user, story=story)
						r.save()
				except Exception as e:
					print(e)
			except:
				s = Site.objects.create(url=request.POST["newSite"], name="{}.{}".format(extracted.domain, extracted.suffix))
				s.user.add(request.user)
				s.save()
			
			os.system("/home2/wrapupne/python2.7/bin/python /home2/wrapupne/wrapupnews/wrapupsite/manage.py update")
			#os.system("python2 manage.py update")
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
				os.system("/home2/wrapupne/python2.7/bin/python /home2/wrapupne/wrapupnews/wrapupsite/manage.py update")
				#os.system("python2 manage.py update")
			except:
				print("Blank Value")
		keys = Keys.objects.filter(user=request.user).all()
	else:
		keys = None
	return render(request, 'wrapup/keyword.html', {'keys':keys})

def register(request):
	if request.method == 'POST':
		u = None
		try:
			u = User.objects.create(username=request.POST["username"], password=make_password(request.POST["userpassword"], salt=None, hasher='default'), email=request.POST["email"])
			#u.save()
			messages.error(request, "I SAID GO AWAY")
		except Exception as e:
			print(e)
			print("Blank Value")
			messages.error(request, "Invalid Request, register failed")
	return render(request, "wrapup/main.html", {'stories': None })

def settings(request):
	print("Debug")
	return render(request, "wrapup/settings.html", {'stories': None })

def delete(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			if request.POST["loc"] == "site":
				site = Site.objects.get(id=request.POST["deleteItem"])
				stories = Stories.objects.filter(user=request.user, site=site.name).all()
				for story in stories:
					story.user.remove(request.user)
					r = Rank.objects.get(user=request.user, story=story)
					r.delete()
				site.user.remove(request.user)
				sites = Site.objects.filter(user=request.user).all()
				return render(request, 'wrapup/site.html', {'sites':sites})
			elif request.POST["loc"] == "keyword":
				key = Keys.objects.get(id=request.POST["deleteItem"])
				key.delete()
				keys = Keys.objects.filter(user=request.user).all()
				return render(request, 'wrapup/keyword.html', {'keys':keys})
	else:
		return render(request, 'wrapup/')
	




