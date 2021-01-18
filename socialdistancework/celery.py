from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdistancework.settings')
app = Celery('socialdistancework')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.beat_schedule = {
    # execute daily at midnight
    'scraping-task-one-min': {
        'task': 'celery_tasks.tasks.hackernews_rss',
        'schedule': crontab(minute=0, hour=0),
    },
    # # executes every 15 minutes
    # 'scraping-task-fifteen-min': {
    #     'task': 'tasks.hackernews_rss',
    #     'schedule': crontab(minute='*/15')
    # },
    # # executes daily at midnight
    # 'scraping-task-midnight-daily': {
    #     'task': 'tasks.hackernews_rss',
    #     'schedule': crontab(minute=0, hour=0)
    # }
}