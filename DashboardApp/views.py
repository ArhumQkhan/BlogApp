import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from PostApp import models as post_models
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

# Create your views here.
@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class DashboardView(View):
  def get(self, request, pk):
    try:
      posts = post_models.Post.objects.filter(status='published').order_by('-created_at')
      user = User.objects.get(pk=pk)
    except Exception as e:
      logger.warning("Error in fetching the object of posts/user in DashboardView")
      return HttpResponse(f"An Error Occured: {e}", status=400)

    return render(request, 'DashboardApp/dashboard.html', {'posts': posts, 'user': user, 'pk': pk})
