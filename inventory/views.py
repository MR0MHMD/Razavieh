from django.shortcuts import render, get_object_or_404
from .models import *


def scrotter_list(request, category=None):
    if category is not None:
        posts = Scrotter.objects.filter(category=category)
    else:
        posts = Scrotter.objects.all()
    context = {'posts': posts}
    return render(request, 'inventory/equipment_list.html', context)


def decorative_list(request):
    posts = Decorative.objects.all()
    context = {'posts': posts}
    return render(request, 'inventory/equipment_list.html', context)


def decorative_detail(request, id):
    post = get_object_or_404(Decorative, id=id)
    context = {'post': post}
    return render(request, 'inventory/equipment_detail.html', context)


def scrotter_detail(request, id):
    post = get_object_or_404(Scrotter, id=id)
    context = {'post': post}
    return render(request, 'inventory/equipment_detail.html', context)

