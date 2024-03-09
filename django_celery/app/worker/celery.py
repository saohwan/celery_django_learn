import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('worker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    task_routes={
        'worker.tasks.dumb': {
            'queue': 'celery'
        },
        'worker.tasks.add': {
            'queue': 'celery'
        }
    }
)

# Rate limiting
app.conf.task_default_rate_limit = '5/m'  # 5 tasks per minute

app.conf.broker_transport_options = {
    'priority_steps': list(range(10)),  # default is 4
    'sep': ':',
    'queue_order_strategy': 'priority',
}

"""
['celery', 'celery1', 'celery2', 'celery3', 'celery4', 'celery5', 'celery6', 'celery7', 'celery8','celery9']
"""

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
