from django.urls import path
from .views import PostListView, PostCreateView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts'),
    path('post-create/', PostCreateView.as_view(), name='post-create'),
]
