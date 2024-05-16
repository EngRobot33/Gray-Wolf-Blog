from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from blog.models import Post


class FieldMixin:
    def dispatch(self, request, *args, **kwargs):
        self.fields = [
            'title', 'slug', 'category', 'status',
            'body', 'thumbnail', 'is_special', 'publish'
        ]
        if request.user.is_superuser:
            self.fields.append("author")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user and post.status == 'b' or post.status == 'd' or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("YOU CAN'T SEE THIS PAGE.")


class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect("login")


class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("YOU CAN'T SEE THIS PAGE.")
