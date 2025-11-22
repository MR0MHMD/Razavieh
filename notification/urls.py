from django.urls import path
from . import views
from .views import create_notification

app_name = 'notification'

urlpatterns = [
    path('notification_list', views.notification_list, name='notification_list'),
    path('notification_list/tags/<int:id>/<slug:slug>/', views.notification_list, name='notification_list_by_tags'),
    path('notification_detail/<int:id>/<slug:slug>', views.notification_detail, name='notification_detail'),
    path('create_notification/', create_notification.as_view(), name='create_notification'),
    path('ajax/create_tag/', views.create_tag_ajax, name='create_tag_ajax'),
]
