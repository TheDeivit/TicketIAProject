from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse

from bson.objectid import ObjectId

from .models import Ticket
from .forms import TicketForm
from bson import ObjectId
from django.contrib.auth import authenticate, login


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
        
    return redirect('ticket:create_ticket')

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
    
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Autenticación exitosa
            login(request, user)
            if user.groups.filter(name='Solicitantes').exists():
                print('Es solicitante')
                # El usuario pertenece al grupo "Solicitantes"
                # Realiza las acciones correspondientes para los solicitantes
                return redirect('ticket:create_ticket')
            else:
                print('Es admin')
                # El usuario no pertenece al grupo "Solicitantes"
                # Realiza otras acciones para usuarios que no sean solicitantes
                return redirect('/admin')
        else:
            # Autenticación fallida
            return render(request, 'ticket/login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'ticket/login.html')
    
#PRIVATE

def _listTicket(request, form):
    tickets = Ticket.objects.order_by('created_at')
    paginator = Paginator(tickets, 7)
    
    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)

    return render(request, 'ticket/index.html', {'tickets':tickets_page, 'form': form})

def landingpage(request):
    return render(request,'ticket/landingpage.html')

def create_ticket(request):
    form = TicketForm()  # Crear una instancia del formulario
    return render(request, 'ticket/create_ticket.html', {'form': form})

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