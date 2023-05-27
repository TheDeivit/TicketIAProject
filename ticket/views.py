from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse

from bson.objectid import ObjectId

from .models import Ticket
from .forms import TicketForm
# Create your views here.

def index(request):
    return _listTicket(request, TicketForm())


def add(request):
    if request.method == 'POST':
        
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return _listTicket(request, form)
        
    return redirect('ticket:index')

def update(request, pk):

    ticket = Ticket.objects.get(pk = ObjectId(pk))

    if request.method == 'POST':

        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
        else:
            return _listTicket(request, form)
        
    return redirect('ticket:index')

def delete(request,pk):

    try:
        ticket = Ticket.objects.get(pk=ObjectId(pk))
        ticket.delete()
    except Ticket.DoesNotExist:
        pass
    
    return redirect('ticket:index')
    
#PRIVATE

def _listTicket(request, form):
    tickets = Ticket.objects.order_by('created_at')
    paginator = Paginator(tickets, 7)
    
    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)

    return render(request, 'ticket/index.html', {'tickets':tickets_page, 'form': form})


#------------ JSON

def jgetTicketId(request,pk):

    try:
        ticket = Ticket.objects.get(pk=ObjectId(pk))
    except Ticket.DoesNotExist:
        return JsonResponse("")
    
    return JsonResponse({
        'name': ticket.name,
        'content': ticket.content
    })