from django.urls import path
from .views import *

urlpatterns = [
  path('posts/', PostListView.as_view(), name='post-list'),
  path('create/', PostCreateView.as_view(), name='post-create'),
  path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
  path('post/<int:pk>/like/', post_like_view, name='post-like'),
]
