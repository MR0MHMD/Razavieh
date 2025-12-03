from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from main.utils import clean_filename
from .forms import *


def post_list(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        'posts': posts,
    }
    return render(request, 'blog/blog/post_list.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('id')
        slug = self.kwargs.get('slug')
        return get_object_or_404(Post, id=post_id, slug=slug)


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
            return render(request, 'report/report/comment_redirect.html', {"report": post})
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


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            # ✔ تغییر نام فایل تصویر
            if "image" in request.FILES:
                post.image = clean_filename(request.FILES["image"])

            post.save()
            form.save_m2m()

            return redirect("blog:post_list")

    else:
        form = PostForm()

    return render(request, "blog/forms/create_post.html", {
        "form": form,
    })
