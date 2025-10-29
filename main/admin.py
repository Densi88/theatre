from django.contrib import admin
from .models import Ticket, Actor, Show, PosterShow, PosterActor, UserProfile


# Register your models here.
@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    pass

@admin.register(Actor)
class AdminActor(admin.ModelAdmin):
    pass

@admin.register(Show)
class AdminShow(admin.ModelAdmin):
    pass

@admin.register(PosterShow)
class AdminPosterShow(admin.ModelAdmin):
    pass

@admin.register(PosterActor)
class AdminPosterActor(admin.ModelAdmin):
    pass

@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    pass


