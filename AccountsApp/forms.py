from django import forms
from .models import Users, Profile

class RegisterForm(forms.ModelForm):
  class Meta:
    model = Users
    fields = ['first_name', 'last_name','username', 'email', 'password']


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
  class Meta:
    model = Users
    fields = ['username', 'email']


class ProfileEditForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['bio']