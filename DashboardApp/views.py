from django.shortcuts import render
from django.views import View
from PostApp import models as post_models

# Create your views here.

class DashboardView(View):
  def get(self, request, pk):
    posts = post_models.Post.objects.filter(status='published').order_by('-created_at')
    return render(request, 'DashboardApp/dashboard.html', {'posts': posts})
