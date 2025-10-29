from django.db.models import Q, Count

from report.models import Comment, Report, CommentReaction
from django.db import models
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.inclusion_tag('report/partials/latest_comments.html', takes_context=True)
def latest_comments(context, count=3):
    """
    آخرین کامنت‌های مربوط به گزارش فعلی را نمایش می‌دهد،
    به همراه واکنش‌های کاربر (like/dislike) اگر لاگین کرده باشد.
    """
    request = context['request']
    report = context.get('report')

    # فقط کامنت‌های فعال همین گزارش
    comments = Comment.objects.filter(report=report, active=True).select_related('name').order_by('-like_count', '-created')[:count]

    # بررسی واکنش‌های کاربر
    user_reactions = {}
    if request.user.is_authenticated:
        user_reactions = dict(
            CommentReaction.objects.filter(user=request.user, comment__in=comments)
            .values_list('comment_id', 'reaction_type')
        )

    # افزودن واکنش به هر کامنت
    for comment in comments:
        comment.user_reaction = user_reactions.get(comment.id)

    return {'latest_comments': comments}


@register.inclusion_tag('main/partials/popular_reports.html')
def top_liked_reports(count=3):
    reports = Report.objects.order_by('-likes', '-created')[:count]
    return {'reports': reports}


@register.inclusion_tag('main/partials/top_commented_reports.html')
def top_commented_reports(count=3):
    reports = Report.objects.all().annotate(
            comments_count=Count('comments', filter=Q(comments__active=True))).order_by('-comments_count', '-date')[:count]
    return {'reports': reports}


@register.inclusion_tag('main/partials/last_reports.html')
def last_reports(count=3):
    reports = Report.objects.order_by('-date')[:count]
    return {'reports': reports}
