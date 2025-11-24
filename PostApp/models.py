from django.db import models
from django.conf import settings
from .constants import POST_STATUS

# Create your models here.
class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
  title = models.CharField(max_length=200)
  content = models.TextField()
  status = models.CharField(choices = POST_STATUS, max_length=20, default='pending')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  like_count = models.PositiveIntegerField(default=0)
  comment_count = models.PositiveIntegerField(default=0)
  is_reported = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.title} - {self.author.username}"


class Attachment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
  file = models.FileField() # this file is supposed to be uploaded to S3 or any cloud storage in production
  uploaded_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    is_reported = models.BooleanField(default=False)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"