from django.urls import path
from . import views


app_name = 'inventory'

urlpatterns = [
    path('Scrotter_list', views.Scrotter_list, name='list'),
    # path('LED_list', views.inventory_list, name='list'),
    # path('Decorative_list', views.inventory_list, name='list'),
]

