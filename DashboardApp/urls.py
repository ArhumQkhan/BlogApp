from django.urls import path, include
from .views import DashboardView, CreateBookView


urlpatterns = [
  path('dashboard/<int:pk>/', DashboardView.as_view(), name='dashboard'),
  path('profile/<int:pk>/create-book', CreateBookView.as_view(), name='create-book'),
  path('', include('AccountsApp.urls')),
  path('', include('PostApp.urls')),
  ]
