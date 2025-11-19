from django.urls import path
from .views import *

urlpatterns = [
  path('posts/', PostListView.as_view(), name='post-list'),
  path('create/', PostCreateView.as_view(), name='post-create'),
  path('posts/<int:pk>', PostDetailView.as_view(), name='post-detail')
]
