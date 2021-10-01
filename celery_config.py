
from celery.schedules import crontab


CELERY_IMPORTS = ('project.tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'project.tasks.update_kalman_placement',
        'schedule': 30.0,
        #'args': (16, 16)
    }
}