from django.shortcuts import render, get_object_or_404
from .forms import *


def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {'post': post}
    return render(request, 'blog/blog/post_detail.html', context)


def post_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, 'blog/forms/comment.html', context)


def post_comment_list(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'blog/blog/comment_list.html', context)
