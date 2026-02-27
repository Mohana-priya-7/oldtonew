import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

#Tells Celery:“Use Django’s settings.py”.Without this → Celery won’t know your project

app=Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
#Automatically finds tasks.py inside:accounts app,products app,any future app.This is VERY IMPORTANT for scalability.