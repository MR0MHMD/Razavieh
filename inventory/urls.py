from django.urls import path
from . import views


app_name = 'inventory'

urlpatterns = [
    path('scrotter_list', views.scrotter_list, name='scrotter_list'),
    path('decorative_list', views.decorative_list, name='decorative_list'),
    path('decorative_detail<int:id>', views.decorative_detail, name='decorative_detail'),
    path('scrotter_detail<int:id>', views.scrotter_detail, name='scrotter_detail'),
    path('category/scrotter_list/<str:category>', views.scrotter_list, name='scrotter_category'),
]

