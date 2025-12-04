from django.shortcuts import render, redirect
from django.views import View
from PostApp import models as post_models
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class DashboardView(View):
  def get(self, request, pk):
    
    posts = post_models.Post.objects.filter(status='published').order_by('-created_at')
    user = User.objects.get(pk=pk)

    return render(request, 'DashboardApp/dashboard.html', {'posts': posts, 'user': user, 'pk': pk})
