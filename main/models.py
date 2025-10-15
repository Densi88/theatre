from django.db import models

class Actors(models.Model):
    actor_name=models.TextField()

class Shows(models.Model):
    title=models.TextField()

class Genres(models.Model):
    genre_name=models.TextField()

class ShowsGenres(models.Model):
    show_id=models.ForeignKey(Shows, on_delete=models.CASCADE)
    genre_id=models.ForeignKey(Genres, on_delete=models.CASCADE)

class Posters(models.Model):
    date=models.DateField()

class PosterShow(models.Model):
    show_id=models.ForeignKey(Shows)
    poster_id=models.ForeignKey(Posters)

class PosterActors(models.Model):
    poster_id=models.ForeignKey(Posters)
    actor_id=models.ForeignKey(Actors)

class Users(models.Model):
    user_name=models.TextField()
    hash_password=models.TextField()

class Tickets(models.Model):
    date=models.DateField()
    row=models.IntegerField()
    seat=models.IntegerField()
    status=models.BooleanField()
    show_id=models.ForeignKey(Shows)
    user_id=models.ForeignKey(Users)


