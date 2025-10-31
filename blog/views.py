from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *


def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {'post': post}
    return render(request, 'blog/blog/post_detail.html', context)


@login_required
def post_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            if request.user.is_authenticated:
                comment.name = request.user
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
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
