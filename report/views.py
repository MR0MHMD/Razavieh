from django.shortcuts import render, redirect, get_object_or_404
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


def report_detail(request, slug):
    report = get_object_or_404(Report, slug=slug)

    # اطمینان از وجود session_key
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # ثبت بازدید فقط یک‌بار در هر session
    viewed_key = f"viewed_report_{report.id}"
    if not request.session.get(viewed_key, False):
        report.views += 1
        report.save(update_fields=['views'])
        request.session[viewed_key] = True

    # بررسی وضعیت لایک برای این کاربر (session)
    liked = ReportLike.objects.filter(report=report, session_key=session_key).exists()
    likes_count = ReportLike.objects.filter(report=report).count()

    context = {
        'report': report,
        'liked': liked,               # آیا کاربر فعلاً این گزارش رو لایک کرده؟
        'likes_count': likes_count,   # تعداد کل لایک‌ها
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

    # اطمینان از وجود سشن
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    liked = False

    # بررسی وجود لایک قبلی برای این سشن و گزارش
    existing_like = ReportLike.objects.filter(report=report, session_key=session_key)

    if existing_like.exists():
        existing_like.delete()
    else:
        ReportLike.objects.create(report=report, session_key=session_key)
        liked = True

    # شمارش دقیق تعداد لایک‌ها از دیتابیس
    likes_count = ReportLike.objects.filter(report=report).count()

    # برای اطمینان از هماهنگی بین صفحات، فیلد likes را هم بروز کن
    report.likes = likes_count
    report.save(update_fields=["likes"])

    # رفرش داده از دیتابیس تا کاملاً دقیق برگرده
    report.refresh_from_db(fields=["likes"])

    return JsonResponse({
        'liked': liked,
        'likes_count': report.likes
    })

@csrf_exempt
def react_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment_id = data.get('comment_id')
        reaction_type = data.get('reaction_type')  # 'like' یا 'dislike'

        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        reacted_comments = request.session.get('reacted_comments', {})

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Comment not found'})

        previous_reaction = reacted_comments.get(str(comment_id))
        user_reaction = None  # برای بازگرداندن وضعیت نهایی به کاربر

        # کاربر همان واکنش را دوباره زده → حذف واکنش
        if previous_reaction == reaction_type:
            if reaction_type == 'like':
                comment.like_count = max(comment.like_count - 1, 0)
            else:
                comment.dislike_count = max(comment.dislike_count - 1, 0)
            reacted_comments.pop(str(comment_id), None)
            user_reaction = None

        else:
            # اگر واکنش متفاوت داده بود → جابجا کنیم
            if previous_reaction == 'like':
                comment.like_count = max(comment.like_count - 1, 0)
            elif previous_reaction == 'dislike':
                comment.dislike_count = max(comment.dislike_count - 1, 0)

            # واکنش جدید
            if reaction_type == 'like':
                comment.like_count += 1
                user_reaction = 'like'
            elif reaction_type == 'dislike':
                comment.dislike_count += 1
                user_reaction = 'dislike'

            reacted_comments[str(comment_id)] = user_reaction

        comment.save()
        request.session['reacted_comments'] = reacted_comments
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'likes': comment.like_count,
            'dislikes': comment.dislike_count,
            'user_reaction': user_reaction  # وضعیت نهایی رو به JS بفرست
        })

    return JsonResponse({'success': False, 'error': 'Invalid request'})
