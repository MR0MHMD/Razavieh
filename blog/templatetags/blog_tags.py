from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/partials/last_comments.html')
def last_comments(post, count=3):
    comments = post.comments.filter(active=True, post=post).select_related('post')[:count]
    return {'comments': comments}


@register.inclusion_tag('blog/partials/last_posts.html')
def last_posts(count=3):
    posts = Post.objects.all()[:count]
    return {'posts': posts}
