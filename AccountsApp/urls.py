from django.urls import path
from .views import LoginView, Registerview, LogoutView, ProfileView, ProfileEditView

urlpatterns = [
  path('', LoginView.as_view(), name='login'),
  path('signup/', Registerview.as_view(), name='register'),
  path('Logout/', LogoutView.as_view(), name='logout'),
  path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
  path('profile/<int:pk>/edit', ProfileEditView.as_view(), name='profile-edit')
]
