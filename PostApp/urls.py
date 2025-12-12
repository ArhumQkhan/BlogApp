from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView, PostEditView, PostDeleteView, SendMailView, download_pdf, post_like_view

urlpatterns = [
  path('posts/', PostListView.as_view(), name='post-list'),
  path('create/', PostCreateView.as_view(), name='post-create'),
  path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
  path('post/<int:pk>/like/', post_like_view, name='post-like'),
  path('post/<int:pk>/edit/', PostEditView.as_view(), name='post-edit'),
  path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
  path('download/pdf/<int:pk>/', download_pdf, name='download_pdf'),
  path("post/<int:pk>/share/", SendMailView.as_view(), name="post-share"),
]
