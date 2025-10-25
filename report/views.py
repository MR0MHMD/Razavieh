from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Greatest
from django.http import JsonResponse
from taggit.models import Tag
from rapidfuzz import fuzz
from .forms import *
import json
import re


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

    liked_reports = []
    if request.user.is_authenticated:
        liked_reports = ReportLike.objects.filter(
            user=request.user
        ).values_list('report_id', flat=True)

    active_comments_count = Comment.objects.filter(active=True).count()

    context = {
        'reports': reports,
        'liked_reports': liked_reports,
        'active_comments_count': active_comments_count
    }
    return render(request, 'report/report/report_list.html', context)


def report_detail(request, slug):
    report = get_object_or_404(Report, slug=slug)

    # ✅ ثبت بازدید با session
    if not request.session.session_key:
        request.session.create()
    viewed_key = f"viewed_report_{report.id}"
    if not request.session.get(viewed_key, False):
        report.views += 1
        report.save(update_fields=['views'])
        request.session[viewed_key] = True

    # ✅ بررسی لایک گزارش (فقط برای کاربران لاگین‌شده)
    liked = False
    if request.user.is_authenticated:
        liked = ReportLike.objects.filter(report=report, user=request.user).exists()

    likes_count = ReportLike.objects.filter(report=report).count()
    active_comments_count = Comment.objects.filter(active=True).count()

    comments = report.comments.select_related('name').order_by('-created')

    if request.user.is_authenticated:
        user_reactions = dict(
            CommentReaction.objects.filter(user=request.user, comment__in=comments)
            .values_list('comment_id', 'reaction_type')
        )
    else:
        user_reactions = {}

    context = {
        'report': report,
        'liked': liked,
        'likes_count': likes_count,
        'active_comments_count': active_comments_count,
    }

    return render(request, 'report/report/report_detail.html', context)


@login_required
def report_comment(request, slug):
    report = get_object_or_404(Report, slug=slug)
    comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.report = report
            comment.user = request.user
            if request.user.is_authenticated:
                comment.name = request.user
            comment.save()
            return redirect(report.get_absolute_url())
    else:
        form = CommentForm()
    context = {
        'report': report,
        'form': form,
        'comment': comment,
    }
    return render(request, 'report/forms/comment.html', context)


def report_comment_list(request, slug):
    report = get_object_or_404(Report, slug=slug)
    comments = report.comments.filter(active=True).select_related('name').order_by('-like_count', '-created')

    # ✅ اگر کاربر لاگین کرده، واکنش‌هایش را برای هر کامنت پیدا کن
    user_reactions = {}
    if request.user.is_authenticated:
        user_reactions = dict(
            CommentReaction.objects.filter(user=request.user, comment__in=comments)
            .values_list('comment_id', 'reaction_type')
        )

    # ✅ افزودن واکنش کاربر به هر کامنت برای استفاده در تمپلیت
    for c in comments:
        c.user_reaction = user_reactions.get(c.id)

    context = {
        'report': report,
        'comments': comments,
    }
    return render(request, 'report/report/comment_list.html', context)


def like_report(request, report_id):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': '/accounts/login/', 'message': 'برای لایک کردن ابتدا وارد شوید.'}, status=401)

    report = get_object_or_404(Report, id=report_id)
    user = request.user

    existing_like = ReportLike.objects.filter(report=report, user=user)
    liked = False

    if existing_like.exists():
        existing_like.delete()
    else:
        ReportLike.objects.create(report=report, user=user)
        liked = True

    likes_count = ReportLike.objects.filter(report=report).count()
    report.likes = likes_count
    report.save(update_fields=["likes"])

    return JsonResponse({
        'liked': liked,
        'likes_count': report.likes
    })


@login_required
def react_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment_id = data.get('comment_id')
            reaction_type = data.get('reaction_type')  # 'like' یا 'dislike'

            # پیدا کردن کامنت
            comment = Comment.objects.get(id=comment_id)

            # بررسی اینکه آیا قبلاً واکنش داده یا نه
            reaction, created = CommentReaction.objects.get_or_create(
                comment=comment,
                user=request.user,
                defaults={'reaction_type': reaction_type}
            )

            if not created:
                # اگر همون واکنش رو دوباره زده بود، حذفش کن
                if reaction.reaction_type == reaction_type:
                    reaction.delete()
                else:
                    # اگه تغییر داده، نوع واکنش رو عوض کن
                    reaction.reaction_type = reaction_type
                    reaction.save()

            # شمارش مجدد لایک و دیسلایک
            comment.like_count = comment.reactions.filter(reaction_type='like').count()
            comment.dislike_count = comment.reactions.filter(reaction_type='dislike').count()
            comment.save(update_fields=['like_count', 'dislike_count'])

            return JsonResponse({
                'success': True,
                'likes': comment.like_count,
                'dislikes': comment.dislike_count,
                'user_reaction': reaction_type
                if CommentReaction.objects.filter(comment=comment, user=request.user,
                                                  reaction_type=reaction_type).exists()
                else None
            })

        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Comment not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def report_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    reports = Report.objects.filter(tags__in=[tag])
    return render(request, 'report/report/report_by_tag.html', {'tag': tag, 'reports': reports})


def normalize_farsi(text):
    if not text:
        return ''
    text = text.strip().lower()
    text = text.replace("ي", "ی").replace("ك", "ک")
    text = re.sub(r"[‌\u200c\s]+", " ", text)
    text = re.sub(r"[^\w\s\u0600-\u06FF]", "", text)
    return text


def report_search(request):
    query = normalize_farsi(request.GET.get('q', '').strip())
    results = []

    if query:
        reports = (
            Report.objects
            .annotate(
                similarity=Greatest(
                    TrigramSimilarity('title', query),
                    TrigramSimilarity('description', query),
                )
            )
            .filter(similarity__gt=0.1)
            .order_by('-similarity')
            .distinct()
        )

        tag_results = Report.objects.filter(
            tags__name__icontains=query
        )

        combined = set(list(reports) + list(tag_results))

        scored_results = []
        for r in combined:
            title_norm = normalize_farsi(r.title)
            desc_norm = normalize_farsi(r.description)
            tags_norm = normalize_farsi(" ".join(t.name for t in r.tags.all()))

            title_score = fuzz.token_sort_ratio(query, title_norm)
            desc_score = fuzz.partial_ratio(query, desc_norm)
            tag_score = fuzz.partial_ratio(query, tags_norm)
            final_score = max(title_score, desc_score, tag_score)

            if final_score > 40:
                scored_results.append((r, final_score))

        results = [r for r, _ in sorted(scored_results, key=lambda x: x[1], reverse=True)]

    return render(request, 'report/report/search_results.html', {
        'query': query,
        'results': results
    })
