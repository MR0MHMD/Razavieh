from django.urls import path
from . import views

app_name = "donation"

urlpatterns = [
    path("donation_list/", views.donation_list, name="donation_list"),
]