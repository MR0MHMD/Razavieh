from django.shortcuts import render, redirect
from .models import Report, ReportImage
from .forms import ReportForm, ReportImageForm


def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        image_form = ReportImageForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()
            files = request.FILES.getlist('image')
            for file in files:
                ReportImage.objects.create(report=report, file=file)
            redirect('')
    else:
        form = ReportForm()
        image_form = ReportImageForm()
        context = {
            'form': form,
            'image_form': image_form
        }
        return render(request, '', context)

