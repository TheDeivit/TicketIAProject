from django.contrib import admin
from .models import Ticket, Location, Urgency, Status, Category, Department, Case
from .forms import TicketForm
from django.contrib.admin import AdminSite

# Register your models here.
admin.site.site_header = 'Ticket IA Admin'
admin.site.site_title = 'Ticket IA Sitio Administrativo'
#Hola
@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    search_fields = ['name']
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

@admin.register(Department)
class AdminDepartment(admin.ModelAdmin):
    pass

@admin.register(Case)
class AdminCase(admin.ModelAdmin):
    pass