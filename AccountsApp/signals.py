from axes.signals import user_locked_out
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .models import Profile

User = get_user_model()

@receiver(user_locked_out)
def locked_out(sender, request, username, **kwargs):
    print(f"User {username} locked out!")

@receiver(post_save, sender=User)
def Profile_Create_View(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)
