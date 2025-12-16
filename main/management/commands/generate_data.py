from django.core.management.base import BaseCommand

from faker import Faker
import random
from datetime import datetime, timedelta

from main.models import Show, News, UserProfile, User, Actor, Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        self.stdout.write(self.style.SUCCESS('Начало генерации данных...'))
        
        # Очистка старых данных (опционально)
        #UserProfile.objects.all().delete()
        Actor.objects.all().delete()
        Genre.objects.all().delete()
        Show.objects.all().delete()
        News.objects.all().delete()
        #User.objects.filter(is_superuser=False).delete()
        
        # 1. Жанры
        genres_data = [
            {'name': 'Драма', 'desc': 'Серьезные пьесы о жизни и отношениях'},
            {'name': 'Комедия', 'desc': 'Веселые и смешные постановки'},
            {'name': 'Трагедия', 'desc': 'Глубокие драмы с печальным концом'},
            {'name': 'Мюзикл', 'desc': 'Спектакли с песнями и танцами'},
            {'name': 'Опера', 'desc': 'Музыкальные драмы с классическим пением'},
            {'name': 'Балет', 'desc': 'Танцевальные постановки без слов'},
            {'name': 'Детектив', 'desc': 'Загадочные истории с расследованием'},
            {'name': 'Мелодрама', 'desc': 'Романтические истории о любви'},
            {'name': 'Фарс', 'desc': 'Гротескные комедии с преувеличениями'},
            {'name': 'Водевиль', 'desc': 'Легкие комедийные пьесы с музыкой'},
        ]
        
        genres = []
        for data in genres_data:
            genre = Genre.objects.create(
                genre_name=data['name'],
                description=data['desc']
            )
            genres.append(genre)
        
        # 2. Актеры
        actors = []
        for _ in range(25):
            gender = random.choice(['male', 'female'])
            if gender == 'male':
                name = fake.name_male()
            else:
                name = fake.name_female()
                
            actor = Actor.objects.create(
                name=name,
                bio=fake.text(max_nb_chars=300),
                photo=None
            )
            actors.append(actor)
        
        # 3. Пользователи
        user_roles = [
        ]
        
        # Добавляем еще случайных пользователей
        for i in range(1000):
            user_roles.append({
                'username': f'user{i}',
                'role': random.choice(['user']),  # чаще user
                'name': fake.name()
            })
        
        for user_data in user_roles:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': f"{user_data['username']}@theatre.ru",
                    'password': 'password123'
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
            
            # Профиль
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': user_data['name'],
                    'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=70),
                    'passport_series': random.randint(1000, 9999),
                    'passport_number': random.randint(100000, 999999),
                    'role': user_data['role']
                }
            )
            
        # 4. Спектакли
        shows_data = [
            {
                'title': 'Горе от ума',
                'desc': 'Классическая комедия Грибоедова о любви и обществе',
                'duration': 150,
                'genres': ['Комедия', 'Драма']
            },
            {
                'title': 'Ревизор',
                'desc': 'Знаменитая комедия Гоголя о чиновниках и обмане',
                'duration': 140,
                'genres': ['Комедия', 'Фарс']
            },
            {
                'title': 'Вишневый сад',
                'desc': 'Лирическая драма Чехова о переменах и ностальгии',
                'duration': 180,
                'genres': ['Драма', 'Трагедия']
            },
            {
                'title': 'Чайка',
                'desc': 'Пьеса Чехова о творчестве, любви и поиске себя',
                'duration': 160,
                'genres': ['Драма']
            },
            {
                'title': 'Ромео и Джульетта',
                'desc': 'Вечная история любви Шекспира',
                'duration': 170,
                'genres': ['Трагедия', 'Драма']
            },
            {
                'title': 'Гамлет',
                'desc': 'Шекспировская трагедия о мести и безумии',
                'duration': 190,
                'genres': ['Трагедия']
            },
            {
                'title': 'Лебединое озеро',
                'desc': 'Знаменитый балет Чайковского',
                'duration': 135,
                'genres': ['Балет']
            },
            {
                'title': 'Свадьба Фигаро',
                'desc': 'Веселая опера Моцарта',
                'duration': 200,
                'genres': ['Опера', 'Комедия']
            },
            {
                'title': 'Король Лир',
                'desc': 'Трагедия Шекспира о власти и семье',
                'duration': 185,
                'genres': ['Трагедия']
            },
            {
                'title': 'Слуга двух господ',
                'desc': 'Итальянская комедия масок',
                'duration': 125,
                'genres': ['Комедия', 'Фарс']
            },
        ]
        
        for show_data in shows_data:
            show = Show.objects.create(
                title=show_data['title'],
                description=show_data['desc'],
                duration=show_data['duration'],
                poster=None,
                available=random.choice([True, True, True, False])  # 75% доступны
            )
            
            # Жанры
            show_genres = Genre.objects.filter(genre_name__in=show_data['genres'])
            show.genre.set(show_genres)
            
            # Актеры (3-6 случайных)
            show_actors = random.sample(actors, random.randint(3, 6))
            show.actor.set(show_actors)
        
        # 5. Новости
        for i in range(12):  # 12 новостей
            months_ago = random.randint(0, 11)
            published_date = datetime.now() - timedelta(days=30*months_ago)
            
            News.objects.create(
                published_at=published_date,
                description=fake.text(max_nb_chars=800),
                news_image=None
            )
        
        self.stdout.write(self.style.SUCCESS('Данные сгенерированы'))