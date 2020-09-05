from django.urls import path
from .views import (PostListView, 
                    PostCreateView, 
                    PostDetailView,
                    PostUpdateView,
                    PostDeleteView,
)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts'),
    path('post-create/', PostCreateView.as_view(), name='post-create'),
    path('post-detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post-update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post-delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
]
