from django.contrib import admin
from .models import Ticket, Actor, Show, UserProfile, Session, Hall


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

@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    pass

@admin.register(Session)
class AdminSession(admin.ModelAdmin):
    pass

@admin.register(Hall)
class AdminHall(admin.ModelAdmin):
    pass



