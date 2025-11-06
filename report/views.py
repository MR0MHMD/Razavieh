from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Greatest
from main.decorators import superuser_required
from django.db.models import Count, Q
from django.http import JsonResponse
from rapidfuzz import fuzz
from typing import Any
from .forms import *
import json
import re


@superuser_required
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


def report_list(request, category=None, tag=None, likes=False, comments=False):
    if comments:
        Report.objects.all().annotate(
            comments_count=Count('comments', filter=Q(comments__active=True))).order_by('-comments_count')
    if likes:
        reports = Report.objects.all().order_by('-likes')
    elif category is not None:
        reports = Report.objects.filter(categories__name=category).annotate(
            comments_count=Count('comments', filter=Q(comments__active=True))).order_by('-date')
    elif tag is not None:
        reports = Report.objects.filter(tags__slug=tag).annotate(
            comments_count=Count('comments', filter=Q(comments__active=True))).order_by('-date')
    else:
        reports = Report.objects.all().annotate(
            comments_count=Count('comments', filter=Q(comments__active=True))).order_by('-date')
    liked_reports = []

    if request.user.is_authenticated:
        liked_reports = ReportLike.objects.filter(
            user=request.user
        ).values_list('report_id', flat=True)

    paginator = Paginator(reports, 9)
    page_number = request.GET.get('page', 1)
    try:
        reports = paginator.page(page_number)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        reports = paginator.page(1)

    context = {
        'reports': reports,
        'liked_reports': liked_reports,
        'category': category,
        'tag': tag,
        'comments': comments,
        'likes': likes,
    }
    return render(request, 'report/report/report_list.html', context)


def report_detail(request, slug):
    report = get_object_or_404(Report, slug=slug)

    if not request.session.session_key:
        request.session.create()
    viewed_key = f"viewed_report_{report.id}"
    if not request.session.get(viewed_key, False):
        report.views += 1
        report.save(update_fields=['views'])
        request.session[viewed_key] = True

    liked = False
    if request.user.is_authenticated:
        liked = ReportLike.objects.filter(report=report, user=request.user).exists()

    likes_count = ReportLike.objects.filter(report=report).count()
    active_comments_count = Comment.objects.filter(active=True, report=report).count()

    comments = report.comments.select_related('name').order_by('-created')

    if request.user.is_authenticated:
        user_reactions: dict[Any, Any] = dict(
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

    user_reactions = {}
    if request.user.is_authenticated:
        user_reactions = dict(
            CommentReaction.objects.filter(user=request.user, comment__in=comments)
            .values_list('comment_id', 'reaction_type')
        )

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
            reaction_type = data.get('reaction_type')

            comment = Comment.objects.get(id=comment_id)

            reaction, created = CommentReaction.objects.get_or_create(
                comment=comment,
                user=request.user,
                defaults={'reaction_type': reaction_type}
            )

            if not created:
                if reaction.reaction_type == reaction_type:
                    reaction.delete()
                else:
                    reaction.reaction_type = reaction_type
                    reaction.save()

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
            .filter(similarity__gt=0.05)
            .order_by('-similarity')
            .distinct()
        )

        tag_results = Report.objects.filter(tags__name__icontains=query)
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

    liked_reports = []
    if request.user.is_authenticated:
        liked_reports = list(
            ReportLike.objects.filter(user=request.user).values_list("report_id", flat=True)
        )

    return render(request, 'report/report/search_results.html', {
        'query': query,
        'results': results,
        'liked_reports': liked_reports,
    })
