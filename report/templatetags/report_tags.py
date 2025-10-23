from django import template
from report.models import Comment

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
