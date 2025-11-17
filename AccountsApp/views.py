from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import Profile, LoginAttempts
from django.utils import timezone #importing timezone for time calculations
from datetime import timedelta #importing timedelta for lockout time calculation
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model #importing get_user_model to get the custom user model
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

User = get_user_model()

# Create your views here.

@receiver(post_save, sender=User)
def Profile_Create_View(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)


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
  LOGIN_ATTEMPT_LIMIT = 3
  LOCKOUT_TIME = timedelta(minutes=1)

  def get(self, request):
    form = LoginForm()
    return render(request, 'AccountsApp/login.html', {'form': form})

  def post(self, request):
    form = LoginForm(request.POST)
    username = request.POST.get('username')
    password = request.POST.get('password')

    user_obj = None

    #checking if user exists in the database
    # user_obj = User.objects.filter(username=username).first() #returns None if user does not exist
    try:
      user_obj = User.objects.get(username=username) # raises DoesNotExist exception if user does not exist
    except User.DoesNotExist:
      messages.error(request, 'User does not exist')
    else:
      if user_obj:
        attempts, created = LoginAttempts.objects.get_or_create(user=user_obj)

        # checking if account is locked
        if attempts.is_locked and attempts.last_failed_at:
          unlock_time = attempts.last_failed_at + self.LOCKOUT_TIME
          if timezone.now() < unlock_time:
            remaining_lock_time = unlock_time - timezone.now()
            messages.error(request, f"You cannot login. Try again after 5 minutes")
            return redirect('login')
          else:
            attempts.is_locked = False
            attempts.failed_attempts = 0
            attempts.last_failed_at = None
            attempts.save()



    # login part
    user = authenticate(request, username=username, password=password)

    if user is not None:
      if user_obj:
        attempts, created = LoginAttempts.objects.get_or_create(user=user)
        attempts.failed_attempts = 0
        attempts.is_locked = False
        attempts.last_failed_at = None
        attempts.save()

      login(request, user)
      messages.success(request, 'Login successful')
      return redirect('profile', pk=user.pk)
    else:

      if user_obj:
        attempts, created = LoginAttempts.objects.get_or_create(user=user_obj)
        attempts.failed_attempts += 1
        attempts.last_failed_at = timezone.now()
        if attempts.failed_attempts >= self.LOGIN_ATTEMPT_LIMIT:
          attempts.is_locked = True
          messages.error(request, "Too many failed attempts. Your account is locked for 5 mins.")
        else:
          messages.error(request, 'Invalid credentials')
        attempts.save()
        return redirect('login')
      else:
        messages.error(request, 'User does not exist')
        return redirect('login')


    # return render(request, 'AccountsApp/login.html', {'form': form, 'user': user_obj})


class LogoutView(View):
  def get(self, request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


class ProfileView(View):
  def get(self, request, pk):
    profile = Profile.objects.get(user__pk=pk)
    return render(request, 'AccountsApp/profile.html', {'profile': profile})

  def put(self, request, pk):
    profile = Profile.objects.get(user__pk=pk)
    bio = request.PUT.get('bio')
    profile.bio = bio
    profile.save()
    messages.success(request, 'Profile updated successfully')
    return redirect('profile', pk=pk)

