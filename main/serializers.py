from rest_framework import serializers
import json

from .models import Show
from .models import News
from .models import Ticket
from .models import Genre
from .models import Actor
from .models import UserProfile
from .models import Session
from .models import Hall
from django.contrib.auth.models import User


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hall
        fields="__all__"


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Actor
        fields="__all__"
    def create(self, validated_data):
        actor = Actor.objects.create(**validated_data)
        return actor

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields="__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model=News
        fields=['id', 'published_at', 'description', 'news_image' ]


    def create(self, validated_data):
        news = News.objects.create(**validated_data)
        return news

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class ShowsSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    actor = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all(), many=True)
    poster = serializers.ImageField(required=False)

    class Meta:
        model = Show
        fields = ['id', 'title', 'description', 'duration', 'genre', 'actor', 'poster', 'available']

    def create(self, validated_data):
        actors = validated_data.pop('actor', [])
        genres = validated_data.pop('genre', [])
        validated_data['available'] = True
        show = Show.objects.create(**validated_data)
        show.actor.set(actors)
        show.genre.set(genres)
        return show

    def update(self, instance, validated_data):
        actors = validated_data.pop('actor', None)
        genres = validated_data.pop('genre', None)

        # обычные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if actors is not None:
            instance.actor.set(actors)
        if genres is not None:
            instance.genre.set(genres)

        return instance

    

class SessionSerializer(serializers.ModelSerializer):
    hall=HallSerializer()
    show=ShowsSerializer()
    class Meta:
        model=Session
        fields=['date', 'show', 'hall_rows', 'hall_seats', 'hall']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model=UserProfile
        fields=['id', 'user', 'passport_number', 'passport_series', 'full_name', 'birth_date']


class TicketSerializer(serializers.ModelSerializer):
    show=SessionSerializer()
    user=UserProfileSerializer()
    class Meta:
        model=Ticket
        fields=['id', 'row', 'seat', 'status', 'price', 'show', 'user']

