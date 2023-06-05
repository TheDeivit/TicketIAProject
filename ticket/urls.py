from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required

app_name='ticket' 

urlpatterns = [
    path('index', login_required(views.index), name='index'),
    path('ticket/add', views.add, name='add'),
    path('ticket/update/<str:pk>', views.update, name='update'),
    path('ticket/delete/<str:pk>', views.delete, name='delete'),
    path('ticket/j-get-ticket-by-id/<str:pk>', views.jgetTicketId),
    # Ruta para la vista de inicio de sesión personalizada
    path('login', views.custom_login, name='login'),
    # Ruta para la vista de cierre de sesión
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    #Ruta para la vista inicial
    path('', views.landingpage, name='landing'),
    path('create_ticket', login_required(views.create_ticket), name='create_ticket'),
]

