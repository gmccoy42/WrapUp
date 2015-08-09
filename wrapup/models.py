from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Site(models.Model):
    url = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    user = models.ManyToManyField(User)

class Keys(models.Model):
	key = models.CharField(max_length=200)
	value = models.IntegerField()
	user = models.ForeignKey(User)

class Stories(models.Model):
	title = models.TextField()
	description = models.TextField()
	link = models.TextField()
	site = models.CharField(max_length=200)
	storyDate = models.DateTimeField()
	prettyDate = models.CharField(max_length=200)
	user = models.ManyToManyField(User)

class Rank(models.Model):
	value = models.IntegerField()
	user = models.ForeignKey(User)
	story = models.ForeignKey(Stories)