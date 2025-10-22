from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import *
import json


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
    return render(request, 'report/forms/create_report.html', context)


def report_list(request):
    reports = Report.objects.all()

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    liked_reports = ReportLike.objects.filter(session_key=session_key).values_list('report_id', flat=True)
    context = {
        'reports': reports,
        'liked_reports': liked_reports,
    }
    return render(request, 'report/report/report_list.html', context)


from django.shortcuts import get_object_or_404
from .models import Report


def report_detail(request, slug):
    report = get_object_or_404(Report, slug=slug)

    # بررسی وجود session_key
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # بررسی اینکه آیا این کاربر قبلاً این گزارش را دیده است یا نه
    viewed_key = f"viewed_report_{report.id}"
    if not request.session.get(viewed_key, False):
        report.views += 1
        report.save(update_fields=['views'])
        request.session[viewed_key] = True

    context = {
        'report': report,
    }
    return render(request, 'report/report/report_detail.html', context)


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
    return render(request, 'report/forms/comment.html', context)


def report_comment_list(request, slug):
    report = get_object_or_404(Report, slug=slug)
    comments = report.comments.filter(active=True)
    context = {
        'report': report,
        'comments': comments,
    }
    return render(request, 'report/report/comment_list.html', context)


def like_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    liked = False

    existing_like = ReportLike.objects.filter(report=report, session_key=session_key)
    if existing_like.exists():
        existing_like.delete()
    else:
        ReportLike.objects.create(report=report, session_key=session_key)
        liked = True

    likes_count = ReportLike.objects.filter(report=report).count()
    return JsonResponse({'liked': liked, 'likes_count': likes_count})
