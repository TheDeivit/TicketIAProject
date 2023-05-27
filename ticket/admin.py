from django.contrib import admin
from .models import Ticket, Location
from .forms import TicketForm
# Register your models here.

@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    form = TicketForm

@admin.register(Location)
class AdminLocation(admin.ModelAdmin):
    pass