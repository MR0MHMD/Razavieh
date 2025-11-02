from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket/', views.ticket, name='ticket'),
    path('about/', views.about, name='about'),
]
