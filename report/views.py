from django.shortcuts import render, redirect, get_object_or_404
from .models import Report, ReportImage
from .forms import ReportForm
from .forms import *

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


def report_detail(request, slug):
    report = get_object_or_404(Report, slug=slug)
    comments = report.comments.all()
    context = {
        'report': report,
        'comments': comments,
    }
    return render(request, 'report/report_detail.html', context)


def report_comment(request, slug):
    report = get_object_or_404(Report, slug=slug)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.report = report
        comment.save()
    context = {
        'report': report,
        'form': form,
        'comment': comment,
    }
    return render(request, 'forms/comment.html', context)


def report_comment_list(request, slug):
    report = get_object_or_404(Report, slug=slug)
    comments = report.comments.all()
    context = {
        'report': report,
        'comments': comments,
    }
    return render(request, 'report/comment_list.html', context)
