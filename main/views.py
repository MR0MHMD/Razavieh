from django.shortcuts import render, redirect
from notification.models import Notification
from .forms import TicketForm
from .models import *


def index(request):
    notifications = Notification.objects.filter(is_active=True).order_by('-date')[:3]
    hero_images = HeroImage.objects.filter(is_active=True)

    context = {
        "notifications": notifications,
        "hero_images": hero_images,
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
                phone=cd['phone'],
                subject=cd['subject']
            )
            return render(request, 'main/partials/ticket_redirect.html')
    else:
        form = TicketForm()
    return render(request, 'main/forms/ticket.html', {'form': form})


def about(request):
    staff = Staff.objects.filter(is_active=True).order_by("order")
    return render(request, 'main/main/about.html', {'staff': staff})


def error_404(request, exception):
    return render(request, 'parent/404.html', status=404)


def error_500(request):
    return render(request, 'parent/500.html', status=500)


def error_403(request, exception):
    return render(request, 'parent/403.html', status=403)
