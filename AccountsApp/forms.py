from django.forms import ModelForm
from .models import Users, Profile

class RegisterForm(ModelForm):
  class Meta:
    model = Users
    fields = ['first_name', 'last_name','username', 'email', 'password']

class LoginForm(ModelForm):
  class Meta:
    model = Users
    fields = ['username', 'password']
