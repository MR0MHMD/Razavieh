from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('create_report/', views.create_report, name='create_report'),
    path('report_list/', views.report_list, name='report_list'),
    path('report_detail/<str:slug>', views.report_detail, name='report_detail'),
    path('repoers/<str:slug>/comment/', views.report_comment, name='report_comment'),
    path('repoers/<str:slug>/comment_list/', views.report_comment_list, name='report_comment_list'),
]
