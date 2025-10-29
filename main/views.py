from django.shortcuts import render, redirect
from report.models import Report
from .forms import TicketForm
from .models import *


def index(request):
    report = Report.objects.filter()
    return render(request, 'main/index.html')


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
