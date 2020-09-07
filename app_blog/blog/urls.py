from django.urls import path
from .views import (PostsListView, 
                    PostCreateView, 
                    PostDetailView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostsListView,
)

urlpatterns = [
    path('posts/', PostsListView.as_view(), name='posts'),
    path('posts/<str:username>', UserPostsListView.as_view(), name='posts-user'),
    path('post-create/', PostCreateView.as_view(), name='post-create'),
    path('post-detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post-update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post-delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
]
