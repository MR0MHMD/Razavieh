from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse_lazy
from .forms import *


class PostListView(ListView):
    model = Post
    template_name = 'blog/blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9


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


class creat_post(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/forms/create_post.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        return super().form_valid(form)
