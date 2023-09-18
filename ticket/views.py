from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse

from bson.objectid import ObjectId

from .models import Ticket, SpecialCase
from .forms import TicketForm
from bson import ObjectId
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError
from django.db.models import Q
import pandas as pd
from ticket.tree import X  # Importa X desde tree.py
import pickle

# Cargar el modelo de árbol de decisión desde el archivo
with open('modelo_arbol.pkl', 'rb') as model_file:
    clf = pickle.load(model_file)

# Create your views here.
def is_tecnico(user):
    return user.groups.filter(name='Tecnicos').exists()

def is_solicitante(user):
    return user.groups.filter(name='Solicitantes').exists()

def is_helpdesk(user):
    return user.groups.filter(name='Helpdesks').exists()

def is_admin(user):
    return user.groups.filter(name='Admins').exists()

@user_passes_test(is_tecnico, login_url='ticket:create_ticket')
def index(request):
    return _listAssignedTickets(request, TicketForm())

def mytickets(request):
    return _listmyTickets(request, TicketForm())

def globaltickets(request):
    return _listGlobalTickets(request, TicketForm())

def specialtickets(request):
    return _listSpecialTickets(request, TicketForm())

# views.py
def asignar_tecnico_predicho(ticket, new_ticket_encoded):
    # Realiza la lógica para obtener el técnico predicho
    # y asígnalo al ticket
    # ... Realiza la predicción utilizando el modelo ...

    # Asigna el técnico predicho al ticket
    predicted_technician = clf.predict(new_ticket_encoded)
    ticket.technician_id = predicted_technician[0]
    ticket.save()

# Definir la función add
def add(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.username = request.user
        
            new_ticket = {
                'urgency_id': ticket.urgency_id,
                'location_id': ticket.location_id,
                'category_id': ticket.category_id,
            }

            # Crear un DataFrame para el nuevo ticket
            new_ticket_df = pd.DataFrame([new_ticket])

            # Realizar la codificación one-hot de las columnas categóricas
            new_ticket_encoded = pd.get_dummies(new_ticket_df, columns=['urgency_id', 'location_id', 'category_id'])
            new_ticket_encoded = new_ticket_encoded.reindex(columns=X.columns, fill_value=0)

            # Realizar la predicción utilizando el modelo y pasar new_ticket_encoded
            asignar_tecnico_predicho(ticket, new_ticket_encoded)
    
            print("TECNICO CON IA: ")
            print(ticket.technician_id)
            print("Fue valido")
        else:
            print("No valido")
            return _listTicket(request, form)
        
    return redirect('ticket:create_ticket')
def update(request, pk):

    ticket = Ticket.objects.get(pk = ObjectId(pk))

    if request.method == 'POST':

        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            technician_id = request.POST.get('technician')  # Obtener el ID del técnico seleccionado
            ticket.technician_id = technician_id
            ticket.save()
        else:
            return _listTicket(request, form)
        
    return redirect('ticket:index')

def updateGlobal(request, pk):

    ticket = Ticket.objects.get(pk = ObjectId(pk))

    if request.method == 'POST':

        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            technician_id = request.POST.get('technician')  # Obtener el ID del técnico seleccionado
            ticket.technician_id = technician_id
            ticket.save()
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
            elif user.groups.filter(name='Admins').exists():
                print('Es admin')
                print(username)
                # El usuario pertenece al grupo "Solicitantes"
                # Realiza las acciones correspondientes para los solicitantes
                return redirect('ticket:admin_panel')
            elif user.groups.filter(name='Superadmins').exists():
                print('Es superadmin')
                print(username)
                # El usuario pertenece al grupo "Solicitantes"
                # Realiza las acciones correspondientes para los solicitantes
                return redirect('/admin')
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

    context = {
        'ticket': ticket,
    }
    #TEST
    print(ticket.name)
    print(ticket.department)
    if ticket.location.name == "Home Office":
        if ticket.status.name == 'Nuevo': 
            print('El ticket debe de ir para tecnico1 y es nuevo')
    #TEST END
    return render(request, 'ticket/myticket_details.html', context)

def ticket_auto(pk):
    ticket = Ticket.objects.get(pk=ObjectId(pk))

    if ticket.department == 'Logistica':
        print('El ticket debe de ir para tecnico1')
    return

def globalticket_details(request, pk):
    ticket = Ticket.objects.get(pk=ObjectId(pk))
    tiempo_para_resolver = ticket.deadline - ticket.created_at
    tiempo_para_resolver_str = str(tiempo_para_resolver)

    context = {
        'ticket': ticket,
        'tiempo_para_resolver_str': tiempo_para_resolver_str,
    }
    return render(request, 'ticket/globalticket_details.html', context)

def specialticket_details(request, pk):
    ticket = Ticket.objects.get(pk=ObjectId(pk))
    return render(request, 'ticket/specialticket_details.html', {'ticket': ticket})

@user_passes_test(is_tecnico, login_url='ticket:create_ticket')
def myassignedtickets_details(request, pk):
    ticket = Ticket.objects.get(pk=ObjectId(pk))
    return render(request, 'ticket/myassignedtickets_details.html', {'ticket': ticket})
#PRIVATE


def _listTicket(request, form):
    tickets = Ticket.objects.order_by('created_at')
    paginator = Paginator(tickets, 8)
    
    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)

    return render(request, 'ticket/index.html', {'tickets':tickets_page, 'form': form})

@login_required(login_url='login')  # Asegúrate de importar 'login_required' desde 'django.contrib.auth.decorators'
def _listmyTickets(request, form):
    search_query = request.GET.get('search')
    username = request.user.id  # Obtén el nombre de usuario actualmente autenticado

    tickets = Ticket.objects.filter(username=username).order_by('created_at')  # Filtra los tickets por nombre de usuario
    tickets_nuevos = Ticket.objects.filter(status__name='Nuevo')
    
    if search_query:
        try:
            ticket_id = ObjectId(search_query)
            tickets = tickets.filter(_id=ticket_id)
            
        except:
            tickets = tickets.filter(
                Q(name__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(location__name__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(urgency__name__icontains=search_query) |
                Q(technician__first_name__icontains=search_query) |
                Q(status__name__icontains=search_query) |
                Q(_id__icontains=search_query)
            )
    paginator = Paginator(tickets, 8)
    num_tickets = tickets.count()
    num_tickets2 = tickets_nuevos.count()

    print( 'HAY ' + str(num_tickets) + ' TICKETS LEVANTADOS')
    print( 'HAY ' + str(num_tickets2) + ' TICKETS NUEVOS LEVANTADOS')
    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)
    
    return render(request, 'ticket/mytickets.html', {'tickets': tickets_page, 'form': form})

@login_required(login_url='login')  # Asegúrate de importar 'login_required' desde 'django.contrib.auth.decorators'
def _listAssignedTickets(request, form):
    search_query = request.GET.get('search')
    technician = request.user.id  # Obtén el nombre de usuario actualmente autenticado

    tickets = Ticket.objects.filter(technician=technician).order_by('created_at')  # Filtra los tickets por nombre de usuario
    if search_query:
        try:
            ticket_id = ObjectId(search_query)
            tickets = tickets.filter(_id=ticket_id)
            
        except:
            tickets = tickets.filter(
                Q(name__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(location__name__icontains=search_query) |
                Q(department__name__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(urgency__name__icontains=search_query) |
                Q(username__first_name__icontains=search_query) |
                Q(status__name__icontains=search_query) |
                Q(_id__icontains=search_query)
            )

    paginator = Paginator(tickets, 8)

    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)
    
    return render(request, 'ticket/index.html', {'tickets': tickets_page, 'form': form})

def _listGlobalTickets(request, form):
    search_query = request.GET.get('search')
    tickets = Ticket.objects.order_by('created_at')

    if search_query:
        try:
            ticket_id = ObjectId(search_query)
            tickets = tickets.filter(_id=ticket_id)
            
        except:
            tickets = tickets.filter(
                Q(name__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(location__name__icontains=search_query) |
                Q(department__name__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(urgency__name__icontains=search_query) |
                Q(username__first_name__icontains=search_query) |
                Q(status__name__icontains=search_query) |
                Q(_id__icontains=search_query)
            )
    paginator = Paginator(tickets, 8)
    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)

    return render(request, 'ticket/globaltickets.html', {'tickets': tickets_page, 'form': form})

def _listSpecialTickets(request, form):
    search_query = request.GET.get('search')
    tickets = Ticket.objects.order_by('created_at')
    special_case_name = "Especial"  # Replace this with the specific name you are looking for
    try:
        special_case = SpecialCase.objects.get(name=special_case_name)
    except SpecialCase.DoesNotExist:
        # Handle the case when the special case doesn't exist
        special_case = None

    if special_case:
        # Filter tickets only for the technician and the specific special case
        tickets = Ticket.objects.filter(specialCase_id=special_case._id).order_by('created_at')
    else:
        # Handle the case when the special case doesn't exist (optional)
        tickets = Ticket.objects.none()

    print('Casos Especiales')
    if search_query:
        try:
            ticket_id = ObjectId(search_query)
            tickets = tickets.filter(_id=ticket_id)
            
        except:
            tickets = tickets.filter(
                Q(name__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(location__name__icontains=search_query) |
                Q(department__name__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(urgency__name__icontains=search_query) |
                Q(username__first_name__icontains=search_query) |
                Q(status__name__icontains=search_query) |
                Q(_id__icontains=search_query)
            )
    paginator = Paginator(tickets, 8)
    page_number = request.GET.get('page')
    tickets_page = paginator.get_page(page_number)

    return render(request, 'ticket/specialtickets.html', {'tickets': tickets_page, 'form': form})

def landingpage(request):
    return render(request,'ticket/landingpage.html')

@user_passes_test(is_solicitante, login_url='ticket:index')
def create_ticket(request):
    #technicians_group = Group.objects.get(name='Tecnicos')
    #technicians = technicians_group.user_set.all()
    form = TicketForm()  # Crear una instancia del formulario
    return render(request, 'ticket/create_ticket.html', {'form': form})


#---------------------ADMIN
def admin_panel(request):
    return render(request, 'ticket/admin_panel.html')

#---------------------- CATALOGOS

#CATALOGO DE CASOS
def cases_index(request):
    specialcases = SpecialCase.objects.all()
    return render(request, 'ticket/cases.html', {'cases': specialcases})






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
        'specialCase_id': str(ticket.specialCase._id),
        'category_id': str(ticket.category._id),
        'department_id': str(ticket.department._id),
        'deadline': ticket.deadline.strftime('%Y-%m-%d'),
        'technician_id': str(ticket.technician.id),
    })