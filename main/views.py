from django.shortcuts import render, redirect
from notification.models import Notification
from .forms import TicketForm
from .models import *


def index(request):
    notifications = Notification.objects.filter(is_active=True).order_by('-datetime')[:3]

    context = {
        "notifications": notifications,
    }
    return render(request, "main/main/index.html", context)


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(
                message=cd['message'],
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject']
            )
            return redirect('blog:post_list')
    else:
        form = TicketForm()
    return render(request, 'main/forms/ticket.html', {'form': form})


def about(request):
    return render(request, 'main/main/about.html')
