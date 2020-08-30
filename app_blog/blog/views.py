from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
)

from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_blog.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'content']
    success_url = '/blog/posts'
    success_message = '%(title)s has been created'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_message(self, title):
        return self.success_message % dict(
            title,
            calculated_field=self.object.title,
        )

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

