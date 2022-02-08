
from celery.schedules import crontab
import os

CELERY_IMPORTS = ('project.tasks' )
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'project.tasks.update_per_interval',
        'schedule': float(os.environ.get("CELERY_BEAT", "1")),
        'options': {'queue' : 'celery_periodic'},
        #'args': (16, 16)
    }
}