from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from main import views

#Написать пути(вроде легко)

router = DefaultRouter()
router.register(r'actors', views.ActorViewSet, basename='actor')
router.register(r'genres', views.GenreViewSet, basename='genre')
router.register(r'shows', views.ShowShowsViewSet, basename='show')
router.register(r'sessions', views.ShowSessionsViewSet, basename='session')
router.register(r'tickets', views.TicketViewSet, basename='ticket')
router.register(r'news', views.ShowNewsViewSet, basename='news')
router.register(r'users', views.UserProfileViewSet, basename='userprofile')

urlpatterns=[
     path('', include(router.urls)),
     # path('api/auth/login/', views.login_view, name='login'),
     path('api/auth/register/', views.register_view, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)