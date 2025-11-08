from django.shortcuts import render
from .models import DonationCard


def donation_list(request):
    cards = DonationCard.objects.filter(is_active=True)
    return render(request, "donation/donation_list.html", {"cards": cards})
