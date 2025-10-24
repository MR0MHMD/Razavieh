from django import template
from report.models import Comment, Report
from django.db import models


register = template.Library()


@register.inclusion_tag('report/partials/latest_comments.html', takes_context=True)
def latest_comments(context, count=3):
    request = context['request']
    comments = Comment.objects.filter(report=context['report'], active=True).order_by('-like_count')[:count]

    # واکنش‌های کاربر از سشن
    reacted_comments = request.session.get('reacted_comments', {})

    for comment in comments:
        comment.user_reaction = reacted_comments.get(str(comment.id), None)

    return {'latest_comments': comments}


@register.inclusion_tag('main/partials/popular_reports.html')
def top_liked_reports(count=3):
    """برگرداندن چند گزارش با بیشترین لایک"""
    reports = Report.objects.order_by('-likes', '-created')[:count]
    return {'reports': reports}


@register.inclusion_tag('main/partials/top_commented_reports.html')
def top_commented_reports(count=3):
    """نمایش چند گزارش با بیشترین کامنت"""
    from report.models import Report  # تا خطاهای import حلقه‌ای پیش نیاد
    reports = Report.objects.annotate(comment_count=models.Count('comments')).order_by('-comment_count', '-created')[:count]
    return {'reports': reports}
