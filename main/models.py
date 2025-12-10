from django.db import models
from django.contrib.auth.models import User

class Actor(models.Model): 
    name=models.TextField(verbose_name="ФИО")
    bio=models.TextField(verbose_name="Биография", blank=True)
    photo=models.ImageField(upload_to='actors/', blank=True, null=True)
    class Meta:
        verbose_name="Актер"
        verbose_name_plural="Актеры" 

class Genre(models.Model):
    genre_name=models.TextField("Название")
    description=models.TextField(verbose_name="Описание жанра")
    class Meta:
        verbose_name="Жанр"
        verbose_name_plural="Жанры"



class Show(models.Model):
    title=models.TextField("Название")
    description=models.TextField("Описание")
    duration=models.IntegerField(verbose_name="Длительность")
    genre=models.ManyToManyField(Genre)
    actor=models.ManyToManyField(Actor)
    poster=models.ImageField(upload_to='')
    available=models.BooleanField()




class Hall(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название зала")
    rows = models.IntegerField(verbose_name="Количество рядов")
    seats_per_row = models.IntegerField(verbose_name="Мест в ряду")



class Session(models.Model):
    date=models.DateTimeField(verbose_name="Время сеанса")
    show=models.ForeignKey(Show, on_delete=models.CASCADE)
    hall_rows=models.IntegerField(default=10)
    hall_seats=models.IntegerField(default=20)
    hall=models.ForeignKey(Hall, on_delete=models.CASCADE)

    class Meta:
        verbose_name="Сеанс"
        verbose_name_plural="Сеансы"



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
    row=models.IntegerField()
    seat=models.IntegerField()
    status=models.BooleanField()
    price=models.IntegerField()
    show=models.ForeignKey(Session, on_delete=models.CASCADE)
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    class Meta:
        verbose_name="Билет"
        verbose_name_plural="Билеты"

class News(models.Model):
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время публикации")
    description=models.TextField()
    news_image=models.ImageField(upload_to='')

