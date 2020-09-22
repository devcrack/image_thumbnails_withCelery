import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_parroter.settings') # Associate a Celery env variable called DJANGO_SETTINGS_MODULE with the django projects settings module.


celery_app = Celery('image_parroter')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')# Updating celery application with settings
celery_app.autodiscover_tasks() # Whe indicate to the new Celery APP instance to auto discover taks within the project
import thumbnailer.task
