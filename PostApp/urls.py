from django.urls import path
from .views import *

urlpatterns = [
  path('', PostListView.as_view(), name='post-list'),
  path('create/', PostCreateView.as_view(), name='post-create'),
]
