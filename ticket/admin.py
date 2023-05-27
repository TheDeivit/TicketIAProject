from django.contrib import admin
from .models import Ticket, Location, Urgency, Status, Category, Subcategory
from .forms import TicketForm
# Register your models here.

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

@admin.register(Subcategory)
class AdminSubcategory(admin.ModelAdmin):
    pass