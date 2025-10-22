from django.db import models
from django.contrib.auth.models import User

class Actor(models.Model): 
    name=models.TextField()
    class Meta:
        verbose_name="Актер"
        verbose_name_plural="Актеры" 

class Show(models.Model):
    title=models.TextField("Название")


class Genre(models.Model):
    genre_name=models.TextField("Название")
    class Meta:
        verbose_name="Жанр"
        verbose_name_plural="Жанры"



class ShowsGenres(models.Model):
    show=models.ForeignKey(Show, on_delete=models.CASCADE)
    genre=models.ForeignKey(Genre, on_delete=models.CASCADE) 


class Poster(models.Model):
    date=models.DateField()
    image=models.ImageField()
    class Meta:
        verbose_name="Афиша"
        verbose_name_plural="Афиши"



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
    full_name=models.TextField("ФИО")
    birth_date=models.DateField()
    class Meta:
        verbose_name="Пользователь"
        verbose_name_plural="Пользователи"


class Ticket(models.Model):
    date=models.DateField()
    row=models.IntegerField()
    seat=models.IntegerField()
    status=models.BooleanField()
    show=models.ForeignKey(Show)
    user=models.ForeignKey(UserProfile)
    class Meta:
        verbose_name="Билет"
        verbose_name_plural="Билеты"


