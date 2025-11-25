from django.urls import path
from .views import *
from DashboardApp.views import DashboardView

urlpatterns = [
  path('', LoginView.as_view(), name='login'),
  path('signup/', Registerview.as_view(), name='register'),
  path('Logout/', LogoutView.as_view(), name='logout'),
  path('dashboard/<int:pk>/', DashboardView.as_view(), name='dashboard'), #From Dashboard app
]
