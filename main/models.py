from django.db import models
from django.contrib.auth.models import User

class Actor(models.Model): #в единственном чиле
    name=models.TextField() #убрать префиксы

class Show(models.Model):
    title=models.TextField()
class Genre(models.Model):
    genre_name=models.TextField()

class ShowsGenres(models.Model):
    show=models.ForeignKey(Show, on_delete=models.CASCADE)
    genre=models.ForeignKey(Genre, on_delete=models.CASCADE) #
class Poster(models.Model):
    date=models.DateField()
    image=models.ImageField()

class PosterShow(models.Model):
    show=models.ForeignKey(Show)
    poster_id=models.ForeignKey(Poster)
    date=models.DateField()
class PosterActor(models.Model):
    poster=models.ForeignKey(Poster)
    actor=models.ForeignKey(Actor)

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    passport_number=models.IntegerField()
    passport_series=models.IntegerField()
    full_name=models.CharField()
    birth_date=models.DateField()

class Ticket(models.Model):
    date=models.DateField()
    row=models.IntegerField()
    seat=models.IntegerField()
    status=models.BooleanField()
    show=models.ForeignKey(Show)
    user=models.ForeignKey(UserProfile)


