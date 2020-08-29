from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                  CreateView,
)

from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostCreateView(LoginRequiredMixin, SuccessMessageMixin,CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    fields = ['title', 'content']
    success_url = '/blog/posts'
    success_message = 'Post has been created'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
