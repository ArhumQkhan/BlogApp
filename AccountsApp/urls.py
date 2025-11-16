from django.urls import path
from .views import *
from DashboardApp.views import DashboardView

urlpatterns = [
  path('', LoginView.as_view(), name='login'),
  path('register/', Registerview.as_view(), name='register'),
  path('Logout/', LogoutView.as_view(), name='logout'),
  path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]
