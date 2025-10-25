from report.models import Comment, Report
from django.db import models
from django import template

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
    reports = Report.objects.order_by('-likes', '-created')[:count]
    return {'reports': reports}


@register.inclusion_tag('main/partials/top_commented_reports.html')
def top_commented_reports(count=3):
    reports = Report.objects.annotate(comment_count=models.Count('comments')).order_by('-comment_count', '-created')[
              :count]
    return {'reports': reports}


@register.inclusion_tag('main/partials/last_reports.html')
def last_reports(count=3):
    reports = Report.objects.order_by('-date')[:count]
    return {'reports': reports}
