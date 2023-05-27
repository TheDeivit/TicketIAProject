from django.shortcuts import render, redirect
from pymongo import MongoClient
from django.core.paginator import Paginator
from django.http import JsonResponse

from bson.objectid import ObjectId

from .models import Ticket, Location
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

        #request.POST._mutable = True
        #request.POST['location'] = ObjectId(request.POST['location'])
        #print(request.POST['location'])

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
    tickets = Ticket.objects.all()
    paginator = Paginator(tickets, 8)
    
    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)

    """#ESTAS LINEAS SIRVEN PARA EL DROPDOWN LIST
    client = MongoClient('localhost', 27017)
    db = client['djangomongo']
    collection = db['ticket_ticket']
    dropdown_data = []
    for document in collection.find():
        dropdown_data.append(document['name'])

    #print(tickets_page)"""

    return render(request, 'ticket/index.html', {'tickets':tickets_page, 'form': form})#, 'dropdown_data': dropdown_data


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