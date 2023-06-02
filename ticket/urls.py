from django.urls import path

from . import views

app_name='ticket' 

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket/add', views.add, name='add'),
    path('ticket/update/<str:pk>', views.update, name='update'),
    path('ticket/delete/<str:pk>', views.delete, name='delete'),
    path('ticket/j-get-ticket-by-id/<str:pk>', views.jgetTicketId),
    path('ticket/get-subcategories/', views.get_subcategories, name='get_subcategories'),

]