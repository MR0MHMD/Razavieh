from django import template
from report.models import Comment

register = template.Library()


@register.inclusion_tag('report/partials/latest_comments.html')
def latest_comments(count=3):
    comments = Comment.objects.select_related('report').order_by('-created')[:count]
    return {'latest_comments': comments}
