from django.urls import path
from .views import *


app_name = 'blog'

urlpatterns = [
    path('post_list/', PostListView.as_view(), name='post_list'),
    path('post_detail/<int:id>/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('post_detail/comment/<slug:slug>', post_comment, name='post_comment'),
    path('post_detail/comment_list/<slug:slug>', post_comment_list, name='post_comment_list'),
    path('creat_post/', creat_post.as_view(), name='creat_post'),
]
