from wrapup.models import Stories
from wrapup.models import Site
from wrapup.models import Keys
from wrapup.models import Rank
from django.http import HttpResponseRedirect
from datetime import datetime
import dateutil.parser
from django.utils.timezone import utc
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import MultipleObjectsReturned
import feedparser
import math
import pytz
from pytz import timezone

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now(pytz.utc)
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"

def check_key(item, u):
	c = 0
	keys = Keys.objects.filter(user=u).all()
	for key in keys:
		c = c + (item.title.count(key.key) * key.value * 50) 
	return math.floor(c)

def checkItem(item):
	try:
		pubDate = dateutil.parser.parse(item["date"])
	except:
		pubDate = dateutil.parser.parse(item["published"])
	pubDate = pubDate.replace(tzinfo=pytz.UTC)
	pubDate = pubDate.astimezone(pytz.utc)

	item["date"] = pubDate
	return item

def dateRank(item):
	try:
		now = datetime.utcnow().replace(tzinfo=utc)
		rank = item.storyDate - now
		rank = rank.total_seconds() / 60 
	except Exception:
		print(item)
	return math.floor(rank)

def getFeed(site):
	feeds = feedparser.parse(site.url)
	entries = []
	count = 0
	for item in feeds[ "items" ]:
		item = checkItem(item)
		try:
			story = Stories.objects.get(link=item["link"])
			story.prettyDate = pretty_date(story.storyDate)
			story.save()
		except MultipleObjectsReturned:
			print("Repeat Deleting")
			stories = Stories.objects.filter(link=item["link"], title=item["title"])
			c = 0
			while (c < len(stories) - 1):
				stories[c].delete()
				c += 1
		except Exception as e:
			s = Stories.objects.create(title=item["title"], link=item["link"], site=site.name, storyDate=item["date"], prettyDate=pretty_date(item["date"]), description=item["description"])
			for user in site.user.all():
				s.user.add(user)
				r = Rank.objects.create(value=0, user=user, story=s)
				r.save()
			count += 1
			s.save()
	return count


class Command(BaseCommand):
    help = 'Updates wrapup'
   
    def handle(self, *args, **options):
    	print("*********************\n*Updating wrapup database*\n*********************")
    	print("Getting Feed")
    	
    	sites = Site.objects.all()
    	for site in sites:
			count = getFeed(site)
			print(site.url + " - " + str(count))

    	ranks = Rank.objects.all()
    	print("\nUpdating Ranks")
    	for rank in ranks:
    		rank.value = dateRank(rank.story) + check_key(rank.story, rank.user)
    		rank.save()
