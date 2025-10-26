from django.urls import path
from . import views
from django.urls import re_path


app_name = 'report'

urlpatterns = [
    path('create_report/', views.create_report, name='create_report'),
    path('report_list/', views.report_list, name='report_list'),
    path('report_list/<str:category>', views.report_list, name='report_list_category'),
    path('report_list/tags/<str:tag>', views.report_list, name='report_list_tag'),
    path('report_detail/<str:slug>/', views.report_detail, name='report_detail'),
    path('repoers/<str:slug>/comment/', views.report_comment, name='report_comment'),
    path('repoers/<str:slug>/comment_list/', views.report_comment_list, name='report_comment_list'),
    path('like/<int:report_id>/', views.like_report, name='like_report'),
    path('react-comment/', views.react_comment, name='react_comment'),
    re_path(r'^tag/(?P<slug>[-\w\u0600-\u06FF]+)/$', views.report_by_tag, name='report_by_tag'),
    path('search/', views.report_search, name='report_search'),
    path('<slug:slug>/', views.report_detail, name='report_detail'),
]

