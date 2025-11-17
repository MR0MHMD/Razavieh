from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('create_report/', views.create_report, name='create_report'),
    path('reports/', views.report_list, name="report_list"),
    path('reports/category/<int:id>/<slug:slug>/', views.report_list, {"mode": "category"}, name="report_list_category"),
    path('reports/tag/<int:id>/<slug:slug>/', views.report_list, {"mode": "tag"}, name="report_list_tag"),
    path('reports/likes/', views.report_list, {"mode": "likes"}, name="report_list_likes"),
    path('reports/comments/', views.report_list, {"mode": "comments"}, name="report_list_comments"),
    path('report_detail/<int:id>/<slug:slug>/', views.report_detail, name='report_detail'),
    path('repoers/<int:id>/<slug:slug>/comment/', views.report_comment, name='report_comment'),
    path('repoers/<int:id>/<slug:slug>/comment_list/', views.report_comment_list, name='report_comment_list'),
    path('like/<int:id>/', views.like_report, name='like_report'),
    path('react-comment/', views.react_comment, name='react_comment'),
    path('search/', views.report_search, name='report_search'),
    path('ajax/create_tag/', views.create_tag_ajax, name='create_tag_ajax'),
]
