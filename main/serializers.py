from rest_framework import serializers

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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields="__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model=News
        fields=['id', 'published_at', 'description', 'news_image' ]

class ShowsSerializer(serializers.ModelSerializer):
    genre=GenreSerializer(many=True)
    actor=ActorSerializer(many=True)
    class Meta:
        model=Show
        fields=['id', 'title', 'description', 'duration', 'genre', 'actor', 'poster', 'available']

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

