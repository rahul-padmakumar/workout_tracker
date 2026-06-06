import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('workout_tracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_transport_options = {
  'priority_steps': list(range(0, 4)),
  'sep': ':',
  'queue_order_strategy': 'priority',
}  # 1 hour
app.autodiscover_tasks()
