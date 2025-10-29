from django.shortcuts import render
from .models import *


def Scrotter_list(request):
    posts = Scrotter.objects.all()
    context = {'posts': posts}
    return render(request, 'inventory/Equipment_list.html', context)
