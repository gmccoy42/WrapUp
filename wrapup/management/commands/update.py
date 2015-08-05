from wrapup.models import Stories
from wrapup.models import Site
from wrapup.models import Keys
from django.http import HttpResponseRedirect
from datetime import datetime
import dateutil.parser
from django.utils.timezone import utc
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import MultipleObjectsReturned
import feedparser
import math

def check_key(item, u):
	c = 0
	keys = Keys.objects.filter(user=u).all()
	for key in keys:
		c = c + (item.title.count(key.key) * key.value)
	return math.floor(c)

def checkItem(item):
	try:
		pubDate = dateutil.parser.parse(item["date"])
	except:
		pubDate = dateutil.parser.parse(item["published"])
	pubDate = pubDate.replace(tzinfo=dateutil.tz.tzutc())
	item["date"] = pubDate
	return item

def dateRank(item):
	try:
		now = datetime.utcnow().replace(tzinfo=utc)
		rank = item.storyDate - now
		rank = rank.total_seconds() / 60 / 60 / 2
	except Exception:
		print(item)
	return math.floor(rank)

def getFeed(url, u, siteName):
	feeds = feedparser.parse(url)
	entries = []
	count = 0
	for item in feeds[ "items" ]:
		item = checkItem(item)
		try:
			story = Stories.objects.get(link=item["link"])
		except MultipleObjectsReturned:
			print("Repeat Deleting")
			stories = Stories.objects.filter(link=item["link"], title=item["title"])
			c = 0
			while (c < len(stories) - 1):
				stories[c].delete()
				c += 1
		except Exception as e:
			s = Stories.objects.create(title=item["title"], link=item["link"], site=siteName, storyDate=item["date"], description=item["description"], rank=0, org_rank=0, user=u)
			s.save()
			count += 1
	return count


class Command(BaseCommand):
    help = 'Updates wrapup'
   
    def handle(self, *args, **options):
    	print("*********************\n*Updating wrapup database*\n*********************")
    	users = User.objects.all()
    	for u in users:
    		print("\nUser - " + u.username + "\n________________")
    		print("Getting Feed")
    		sites = Site.objects.filter(user=u).all()
    		for site in sites:
    			count = getFeed(site.url, u, site.name)
    			print(u.username + " - " + site.url + " - " + str(count))

    	stories = Stories.objects.all()
    	print("\nUpdating Ranks")
    	for story in stories:
			story.rank = dateRank(story) + check_key(story, u)
			story.save()
