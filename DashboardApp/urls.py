from django.urls import path, include
from .views import DashboardView


urlpatterns = [
  path('dashboard/<int:pk>/', DashboardView.as_view(), name='dashboard'),
  path('', include('AccountsApp.urls')),
  path('', include('PostApp.urls')),
  ]
