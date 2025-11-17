from report.models import Comment, Report, CommentReaction, ReportLike
from django.db.models import Q, Count
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.inclusion_tag('report/partials/latest_comments.html', takes_context=True)
def latest_comments(context, count=3):
    """کامنت‌های آخر هر گزارش + واکنش‌های کاربر"""
    request = context['request']
    report = context.get('report')

    comments = Comment.objects.filter(report=report, active=True).select_related('name').order_by('-like_count',
                                                                                                  '-created')[:count]

    # بررسی واکنش‌های کاربر
    user_reactions = {}
    if request.user.is_authenticated:
        user_reactions = dict(
            CommentReaction.objects.filter(user=request.user, comment__in=comments)
            .values_list('comment_id', 'reaction_type')
        )

    for comment in comments:
        comment.user_reaction = user_reactions.get(comment.id)

    return {'latest_comments': comments}


# 🔹 آخرین گزارشات
@register.inclusion_tag('partials/report_cards.html', takes_context=True)
def last_reports(context, count=3):
    """آخرین گزارش‌ها"""
    user = context['request'].user
    reports = Report.objects.annotate(
        comments_count=Count('comments', filter=Q(comments__active=True))
    ).order_by('-date')[:count]

    liked_reports = []
    if user.is_authenticated:
        liked_reports = ReportLike.objects.filter(user=user).values_list('report_id', flat=True)

    return {'reports': reports, 'liked_reports': liked_reports}


# 🔹 پرلایک‌ترین گزارشات
@register.inclusion_tag('partials/report_cards.html', takes_context=True)
def top_liked_reports(context, count=3):
    """محبوب‌ترین گزارش‌ها"""
    user = context['request'].user
    reports = Report.objects.annotate(
        comments_count=Count('comments', filter=Q(comments__active=True))).order_by('-likes', '-created')[:count]

    liked_reports = []
    if user.is_authenticated:
        liked_reports = ReportLike.objects.filter(user=user).values_list('report_id', flat=True)

    return {'reports': reports, 'liked_reports': liked_reports}


# 🔹 پربحث‌ترین گزارشات
@register.inclusion_tag('partials/report_cards.html', takes_context=True)
def top_commented_reports(context, count=3):
    """پربحث‌ترین گزارش‌ها"""
    user = context['request'].user
    reports = Report.objects.annotate(
        comments_count=Count('comments', filter=Q(comments__active=True))
    ).order_by('-comments_count', '-date')[:count]

    liked_reports = []
    if user.is_authenticated:
        liked_reports = ReportLike.objects.filter(user=user).values_list('report_id', flat=True)

    return {'reports': reports, 'liked_reports': liked_reports}
