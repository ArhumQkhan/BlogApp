from django import forms
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name','username', 'email', 'password']


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email']


class ProfileEditForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['bio']