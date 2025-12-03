from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import Profile
from django.contrib.auth import get_user_model #importing get_user_model to get the custom user model
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class Registerview(View):
  def get(self, request):
    form = RegisterForm()
    return render(request, 'AccountsApp/register.html', {'form': form})

  def post(self, request):
    form = RegisterForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      email = form.cleaned_data.get('email')
      password = form.cleaned_data.get('password')

      User.objects.create_user(username=username, email=email, password=password)
      messages.success(request, 'Registration successful')
      return redirect('login')
    return render(request, 'AccountsApp/register.html', {'form': form})


@method_decorator([csrf_protect, never_cache], name='dispatch')
class LoginView(View):

  def get(self, request):
    request.session.flush()
    form = LoginForm()
    return render(request, 'AccountsApp/login.html', {'form': form})

  def post(self, request):
    form = LoginForm(request.POST)
    
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')

      user =  authenticate(request=request, username=username, password=password)
         
      if user:

        login(request, user)
        messages.success(request, "Login Successful")
        return redirect('dashboard', pk=user.pk)
      
      else:

          messages.error(request, "Invalid username/password")
          return redirect('login')


@method_decorator(never_cache, name='dispatch')
class LogoutView(View):
  def get(self, request):

    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class ProfileView(View):
  def get(self, request, pk):
    profile = Profile.objects.get(user__pk=pk)
    return render(request, 'AccountsApp/profile.html', {'profile': profile})


@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class ProfileEditView(View):
  def get(self, request):
    user_form = UserEditForm(instance=request.user)
    bio_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'AccountsApp/profile_edit.html', {'user_form': user_form, 'bio_form': bio_form})
  
  def post(self, request):
    user_form = UserEditForm(request.POST, instance=request.user)
    bio_form = ProfileEditForm(request.POST, instance=request.user.profile)

    if user_form.is_valid() and bio_form.is_valid():
      user_form.save()
      bio_form.save()
      return redirect('profile', pk=request.user.pk)

    return render(request, 'AccountsApp/profile_edit.html', {'user_form': user_form, 'bio_form': bio_form})