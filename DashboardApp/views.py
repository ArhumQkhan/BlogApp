import logging
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from PostApp import models as post_models
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import BookForm

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
      logger.error("Error in fetching the object of posts/user in DashboardView")
      return HttpResponse(f"An Error Occured: {e}", status=400)

    return render(request, 'DashboardApp/dashboard.html', {'posts': posts, 'user': user, 'pk': pk})


class CreateBookView(View):

  def get(self, request):

    try:
      form = BookForm()
    except Exception as e:
      logger.error("Error in fetching the user object in CreateBookView")
      return HttpResponse(f"An Error occured: {e}", status=400)
    
    return render(request, "DashboardApp/create_books.html", {'form': form})
  
  def post(self, request, pk):
    
    form = BookForm(request.POST, request.FILES)

    if form.is_valid():
      form.save()
      messages.success(request, "Your Book is up for sale")
      return redirect('profile', pk=pk)