from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse

from bson.objectid import ObjectId

from .models import Ticket
from .forms import TicketForm
from bson import ObjectId
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
def is_tecnico(user):
    return user.groups.filter(name='Tecnicos').exists()

def is_solicitante(user):
    return user.groups.filter(name='Solicitantes').exists()

def is_helpdesk(user):
    return user.groups.filter(name='Helpdesks').exists()

@user_passes_test(is_tecnico, login_url='ticket:create_ticket')
def index(request):
    return _listTicket(request, TicketForm())

def mytickets(request):
    return _listmyTickets(request, TicketForm())

def globaltickets(request):
    return _listGlobalTickets(request, TicketForm())

def add(request):
    if request.method == 'POST':
        
        form = TicketForm(request.POST)#, request.FILES
        if form.is_valid():
            form = form.save(commit=False)
            form.username = request.user
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

def updateGlobal(request, pk):

    ticket = Ticket.objects.get(pk = ObjectId(pk))

    if request.method == 'POST':

        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
        else:
            return _listGlobalTickets(request, form)
        
    return redirect('ticket:globaltickets')

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
            elif user.groups.filter(name='Tecnicos').exists():
                print('Es tecnico')
                print(username)
                # El usuario pertenece al grupo "Solicitantes"
                # Realiza las acciones correspondientes para los solicitantes
                return redirect('ticket:index')
            elif user.groups.filter(name='Helpdesks').exists():
                print('Es helpdesk')
                print(username)
                # El usuario pertenece al grupo "Solicitantes"
                # Realiza las acciones correspondientes para los solicitantes
                return redirect('ticket:globaltickets')
            else:
                return render(request, 'ticket/login.html')
        else:
            # Autenticación fallida
            return render(request, 'ticket/login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'ticket/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')  # Cambia 'login' por la URL a la que deseas redirigir después del cierre de sesión

@user_passes_test(is_tecnico, login_url='ticket:create_ticket')
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=ObjectId(pk))
    return render(request, 'ticket/ticket_details.html', {'ticket': ticket})

@user_passes_test(is_solicitante, login_url='ticket:index')
def myticket_details(request, pk):
    ticket = Ticket.objects.get(pk=ObjectId(pk))
    return render(request, 'ticket/myticket_details.html', {'ticket': ticket})

def globalticket_details(request, pk):
    ticket = Ticket.objects.get(pk=ObjectId(pk))
    return render(request, 'ticket/globalticket_details.html', {'ticket': ticket})
#PRIVATE


def _listTicket(request, form):
    tickets = Ticket.objects.order_by('created_at')
    paginator = Paginator(tickets, 6)
    
    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)

    return render(request, 'ticket/index.html', {'tickets':tickets_page, 'form': form})

@login_required(login_url='login')  # Asegúrate de importar 'login_required' desde 'django.contrib.auth.decorators'
def _listmyTickets(request, form):
    username = request.user.id  # Obtén el nombre de usuario actualmente autenticado

    tickets = Ticket.objects.filter(username=username).order_by('created_at')  # Filtra los tickets por nombre de usuario
    paginator = Paginator(tickets, 6)

    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)

    return render(request, 'ticket/mytickets.html', {'tickets': tickets_page, 'form': form})

def _listGlobalTickets(request, form):
    tickets = Ticket.objects.order_by('created_at')
    paginator = Paginator(tickets, 6)
    
    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)

    return render(request, 'ticket/globaltickets.html', {'tickets':tickets_page, 'form': form})

def landingpage(request):
    return render(request,'ticket/landingpage.html')

@user_passes_test(is_solicitante, login_url='ticket:index')
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
        'content': ticket.content,
        'location_id': str(ticket.location._id),
        'urgency_id': str(ticket.urgency._id),
        'status_id': str(ticket.status._id),
        'category_id': str(ticket.category._id),
        'department_id': str(ticket.department._id),
        'deadline': ticket.deadline.strftime('%Y-%m-%d'),
    })