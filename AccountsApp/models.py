from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import USER_ROLE
from django.conf import settings

# Create your models here.

class Users(AbstractUser):
  
  role = models.CharField(choices = USER_ROLE, default = 'User', max_length=10)
  is_email_verified = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.username

class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='profile') #i am using AUTH_USER_MODEL here to make it future proof, everytime the user model changes in settings, it will automatically show here
  bio = models.TextField(blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Profile of {self.user.username}"
