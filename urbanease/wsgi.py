"""
WSGI config for UrbanEase project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urbanease.settings')

application = get_wsgi_application() 