from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('post_list/', views.post_list, name='post_list'),
    path('post_detail/<str:slug>', views.post_detail, name='post_detail'),
    path('post_detail/<str:slug>/comment', views.post_comment, name='post_comment'),
    path('post_detail/<str:slug>/comment_list', views.post_comment_list, name='post_comment_list'),
]
