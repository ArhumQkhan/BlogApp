from celery import Celery
from celery.schedules import crontab
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogProject.settings')

app = Celery('BlogProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # looks for tasks.py in all installed apps

# app.conf.beat_schedule = {
#     "send-posts-midnight": {
#         "task": "PostApp.tasks.send_user_new_posts",
#         "schedule": crontab(hour=0, minute=0),  # runs daily at midnight
#     }
# }

app.conf.beat_schedule = {
    "send-posts-every-2-mins": {
        "task": "PostApp.tasks.send_user_new_posts",
        "schedule": 120.0,  # 120 seconds
    }
}
