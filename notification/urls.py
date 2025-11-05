from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('notification_list', views.notification_list, name='notification_list'),
    path('notification_list/tags/<str:tag>', views.notification_list, name='notification_list_by_tags'),
    path('notification_detail/<int:pk>/', views.notification_detail, name='notification_detail'),
    path('create_notification/', views.create_notification, name='create_notification'),
]
