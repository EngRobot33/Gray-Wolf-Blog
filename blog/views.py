from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from account.mixins import AuthorAccessMixin
from account.models import User
from .models import Post, Category


class PostList(ListView):
    queryset = Post.objects.published()
    paginate_by = 10


class PostDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Post.objects.published(), slug=slug)


class PostPreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Post, pk=pk)


class CategoryList(ListView):
    paginate_by = 5
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.posts.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 5
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.posts.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
