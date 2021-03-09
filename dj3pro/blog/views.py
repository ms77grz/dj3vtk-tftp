from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


# def post_list(request):
#     # posts = Post.published.all()
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3) # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     # return render(request, 'blog/post/list.html', {'posts': posts})
#     return render(request, 'blog/post/list.html', {'title':'Blog','posts': posts, 'page': page})


class PostListView(LoginRequiredMixin, ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    # template_name = 'blog/post/list.html'


# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(Post,  slug=post, 
#                                     status='published',
#                                     publish__year=year,
#                                     publish__month=month,
#                                     publish__day=day)
#     return render(request, 'blog/post/detail.html', {'title': post.title, 'post': post})


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-publish')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    # query_pk_and_slug = True
    # template_name = 'blog/post/detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body']
    # success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
