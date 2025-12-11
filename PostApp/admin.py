from django.contrib import admin
from .models import Post, Comment, LikedPost

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikedPost)
