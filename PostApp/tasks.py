from celery import shared_task
from .models import Post
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

User = get_user_model()

# @shared_task
# def send_user_new_posts():
#     now = timezone.now()
#     yesterday = now - timedelta(days=1)

#     new_posts = Post.objects.filter(created_at__gte=yesterday)
#     users = User.objects.all()

#     if not new_posts.exists():
#         return "No new posts"
    
#     for user in users:
#         if not user.email:
#             continue
#         subject = f"Todays new post {now}"
#         message = "\n\n".join([f"{post.title}\n{post.content}" for post in new_posts])

#         try:
#             send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email="arhum.qayyum@devsinc.com",
#                 recipient_list=["khanarhumqayyum@gmail.com"],
#             )
#         except Exception as e:
#             print(f"Error sending email to {user.email}: {e}")

@shared_task
def send_user_new_posts():
    now = timezone.now()
    five_minutes_ago = now - timedelta(minutes=2)  # changed for testing

    new_posts = Post.objects.filter(created_at__gte=five_minutes_ago)
    users = User.objects.all()

    if not new_posts.exists():
        return "No new posts"
    
    for user in users:
        if not user.email:
            continue
        
        subject = f"New posts in last 5 minutes ({now})"
        message = "\n\n".join([f"{post.title}\n{post.content}" for post in new_posts])

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email="arhum.qayyum@devsinc.com",
                recipient_list=[user.email],  # send to the actual user
            )
        except Exception as e:
            print(f"Error sending email to {user.email}: {e}")