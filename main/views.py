from django.shortcuts import render
from report.models import Report


def index(request):
    report = Report.objects.filter()
    return render(request, 'main/index.html')
