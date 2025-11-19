from django.urls import path, include
from AccountsApp.views import ProfileView


urlpatterns = [
  path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
  path('', include('AccountsApp.urls')),
  path('', include('PostApp.urls')),
  ]
