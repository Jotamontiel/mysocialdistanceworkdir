from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialdistancework.settings')
app = Celery('socialdistancework')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.beat_schedule = {
    # Execute: every 3 hours
    'scraping-hackernews-task-every-three-hours': {
        'task': 'celery_tasks.tasks.hackernews_rss',
        'schedule': crontab(minute=0, hour='*/3'),
    },
    # Execute: daily at midnight
    'scraping-nytimesnews-task-daily-at-midnight-with-30-min': {
        'task': 'celery_tasks.tasks.nytimesnews_mostpopular_viewed_api_scraper',
        'schedule': crontab(minute=30, hour=0),
    },
    # Execute: monthly
    'sftp-download-liketrading-tikers-monthly': {
        'task': 'celery_tasks.tasks.liketrading_download_tickers',
        'schedule': crontab(minute=12, hour='*/5'),
    },
}