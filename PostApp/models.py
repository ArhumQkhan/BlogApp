from django.db import models
from django.conf import settings
from .constants import POST_STATUS
from ckeditor.fields import RichTextField
from PIL import Image

# Create your models here.
class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
  title = models.CharField(max_length=200)
  post_image = models.ImageField(null=True, blank=True, upload_to="images/")
  post_doc = models.FileField(null=True, blank=True, upload_to="docs/")
  content = RichTextField(blank=True, null=True)
  status = models.CharField(choices = POST_STATUS, max_length=20, default='published')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  comment_count = models.PositiveIntegerField(default=0)
  is_reported = models.BooleanField(default=False)
  likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likedposts", through="LikedPost")

  def __str__(self):
    return f"{self.title} - {self.author.username}"
  
  #------------ Image Resizing --------------
  
  def save(self, *args, **kwargs):
     super().save(*args, **kwargs) #first we will save the object

     if self.post_image:
        image_path = self.post_image.path
        img = Image.open(image_path)

        max_size = (800, 800) # width, height
        img.thumbnail(max_size) # resizing while keeping the aspect ratio
        img.save(image_path)



class LikedPost(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
     return f'{self.user.username} - {self.post.title}'
  

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
    