from django.shortcuts import render, redirect
from .models import Report, ReportImage
from .forms import ReportForm, ReportImageForm


def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()

            files = request.FILES.getlist('image')
            for f in files:
                ReportImage.objects.create(report=report, image=f)

            return redirect('report:report_list')
    else:
        form = ReportForm()

    context = {
        'form': form,
    }
    return render(request, 'forms/create_report.html', context)


def report_list(request):
    reports = Report.objects.all()
    return render(request, 'report/report_list.html', {'reports': reports})

