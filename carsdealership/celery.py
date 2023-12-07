from __future__ import absolute_import, unicode_literals
import logging
import os
from celery import Celery
from celery.schedules import crontab

# from autosalons.tasks import ShowroomsBuyingCarTask

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carsdealership.settings')

app = Celery('carsdealership')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.conf.beat_schedule = {
    'showrooms_buying_car': {
        'task': 'autosalons.tasks.run_showrooms_buying_car_task',
        'schedule': crontab(minute='*/1'),
    },
    'showrooms_update_suppliers': {
        'task': 'autosalons.tasks.showrooms_update_suppliers',
        'schedule': crontab(minute='*/1'),
    },
    'customers_buying_car': {
        'task': 'autosalons.tasks.run_customers_buying_car_task',
        'schedule': crontab(minute='*/1'),
    },
}

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print('__________________')
#     logger.info(f"Starting ")
#     print(f'Request: {self.request!r}')
