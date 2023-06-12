from django.contrib import admin
from .models import Ticket, Location, Urgency, Status, Category
from .forms import TicketForm
from django.contrib.admin import AdminSite

# Register your models here.
admin.site.site_header = 'Ticket IA Administration'
admin.site.site_title = 'Ticket IA Admin Site'

@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    form = TicketForm

@admin.register(Location)
class AdminLocation(admin.ModelAdmin):
    pass

@admin.register(Urgency)
class AdminUrgency(admin.ModelAdmin):
    pass

@admin.register(Status)
class AdminStatus(admin.ModelAdmin):
    pass

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    pass
