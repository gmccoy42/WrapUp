from django.contrib.auth.models import User
from wrapup.models import Keys, Site, Stories, Rank
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = { 'password': {'write_only': True }}

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class KeysSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Keys
        fields = ('id', 'key', 'value', 'user')

    def create(self, validated_data):
        key = Keys(key=validated_data['key'], value=validated_data['value'], user=validated_data['user'])
        key.save()
        return key

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Site
        fields = ('id', 'url', 'name', 'user')

    def create(self, validated_data):
        site = Site(url=validated_data['url'], name=validated_data['name'], user=validated_data['user'])
        site.save()
        return site

class StoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stories
        fields = ('id', 'title', 'description', 'link', 'site', 'storyDate', 'prettyDate', 'user')

    def create(self, validated_data):
        stories = Stories(
                title=validated_data['title'],
                name=validated_data['description'],
                link=validated_data['link'],
                site=validated_data['site'],
                storyDate=validated_data['storyDate'],
                prettyDate=validated_data['prettyDate'],
                user=validated_data['user'],
            )
        stories.save()
        return stories

class RankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rank
        fields = ('id', 'value', 'user', 'story')
