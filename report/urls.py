from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

app_name = 'report'

urlpatterns = [
    path('create_report/', views.create_report, name='create_report'),
    path('report_list/', views.report_list, name='report_list'),
]
