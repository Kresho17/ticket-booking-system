from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configure our Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_booking_system.settings')

app = Celery('ticket_booking_system')

# Configure the broker, e.g. Redis
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically loads tasks.py files in all applications
app.autodiscover_tasks()
