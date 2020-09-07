from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView,
)

from .models import Post

class PostsListView(ListView):
    model = Post
    template_name = 'blog/posts_blog.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class UserPostsListView(ListView):
    model = Post
    template_name = 'blog/posts_user.html'
    context_object_name = 'posts'

    def get_queryset(self,):
        super(UserPostsListView, self).get_queryset()
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.all().filter(author=user).order_by('-date_posted')
    

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
        # super(PostCreateView, self).get_success_message(cleaned_data=title)
        return self.success_message % dict(
            title,
            calculated_field=self.object.title,
        )

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_update.html'
    success_message = '%(title)s has been Updated'

    def get_success_message(self, title):
        return self.success_message % dict(
            title,
            calculated_field=self.object.title,
        )

    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = '/blog/posts'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False