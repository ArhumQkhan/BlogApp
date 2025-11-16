from django.contrib import admin
from .models import Users, Profile, LoginAttempts

# Register your models here.
admin.site.register(Users)
admin.site.register(Profile)
