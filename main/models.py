from django.db import models

class Actors(models.Model): #в единственном чиле
    name=models.TextField() #убрать префиксы

class Shows(models.Model):
    title=models.TextField()

class Genres(models.Model):
    genre_name=models.TextField()

class ShowsGenres(models.Model):
    show=models.ForeignKey(Shows, on_delete=models.CASCADE)
    genre=models.ForeignKey(Genres, on_delete=models.CASCADE) #

class Posters(models.Model):
    date=models.DateField()
    image=models.ImageField()

class PosterShow(models.Model):
    show=models.ForeignKey(Shows)
    poster_id=models.ForeignKey(Posters)
    #Добавить дату


class PosterActors(models.Model):
    poster_id=models.ForeignKey(Posters)
    actor_id=models.ForeignKey(Actors)


class Tickets(models.Model):
    date=models.DateField()
    row=models.IntegerField()
    seat=models.IntegerField()
    status=models.BooleanField()
    show_id=models.ForeignKey(Shows)
    user_id=models.ForeignKey()#добавить юзера и его расширение


