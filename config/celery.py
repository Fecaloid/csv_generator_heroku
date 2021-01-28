from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery = Celery(
    'config',
    include=['apps.task.generator']
)

celery.config_from_object('django.conf:settings')
# celery.conf.update(
#     BROKER_URL=os.environ['REDIS_URL'],
#     CELERY_RESULT_BACKEND=os.environ['REDIS_URL']
# )


celery.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    celery.start()
