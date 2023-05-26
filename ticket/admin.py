from django.contrib import admin
from .models import Ticket, Location
# Register your models here.

@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    pass

@admin.register(Location)
class AdminLocation(admin.ModelAdmin):
    pass
