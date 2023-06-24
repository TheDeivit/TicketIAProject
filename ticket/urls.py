from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required

app_name='ticket' 

urlpatterns = [
    path('index', login_required(views.index), name='index'),
    path('ticket/add', views.add, name='add'),
    path('ticket/update/<str:pk>', views.update, name='update'),
    path('ticket/updateglobal/<str:pk>', views.updateGlobal, name='updateglobal'),
    path('ticket/delete/<str:pk>', views.delete, name='delete'),
    path('ticket/j-get-ticket-by-id/<str:pk>', views.jgetTicketId),
    # Ruta para la vista de inicio de sesión personalizada
    path('login', views.custom_login, name='login'),
    # Ruta para la vista de cierre de sesión
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    #Ruta para la vista inicial
    path('', views.custom_login, name='login'),
    path('create_ticket', login_required(views.create_ticket), name='create_ticket'),
    path('logout/', views.logout_view, name='logout'),
    path('ticket/details/<str:pk>', views.ticket_details, name='ticket_details'),
    path('myticket/details/<str:pk>', views.myticket_details, name='myticket_details'),
    path('ticket/mytickets', views.mytickets, name='mytickets'),
    path('globalticket/details/<str:pk>', views.globalticket_details, name='globalticket_details'),
    path('ticket/globaltickets', views.globaltickets, name='globaltickets'),
    #path('ticket/user_index', views.user_index, name='user_index'),

]