from django.shortcuts import render
from django.views import View
from PostApp import models as post_models
from AccountsApp import models as account_models

# Create your views here.

class DashboardView(View):
  def get(self, request, pk):
    posts = post_models.Post.objects.filter(status='published').order_by('-created_at')
    user = account_models.Users.objects.get(pk=pk)

    if posts is None:
      render(request, 'DashboardApp/dashboard.html', {'message': 'No posts available.', 'pk': pk})
    return render(request, 'DashboardApp/dashboard.html', {'posts': posts, 'user': user, 'pk': pk})
