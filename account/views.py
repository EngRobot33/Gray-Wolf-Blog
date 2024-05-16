from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.models import Post
from .forms import ProfileForm
from .mixins import FieldMixin, FormValidMixin, SuperUserAccessMixin, AuthorsAccessMixin
from .models import User


class PostList(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        else:
            return Post.objects.filter(author=self.request.user)


class PostCreate(AuthorsAccessMixin, FormValidMixin, FieldMixin, CreateView):
    model = Post
    template_name = 'registration/post_create_update.html'


class PostUpdate(LoginRequiredMixin, FormValidMixin, FieldMixin, UpdateView):
    model = Post
    template_name = 'registration/post_create_update.html'


class PostDelete(SuperUserAccessMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('account:home')
    template_name = 'registration/post_confirm_delete.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy("account:home")
        else:
            return reverse_lazy("account:profile")
