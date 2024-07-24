"""
WSGI config for access_files project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'access_files.settings')

application = get_wsgi_application()

from django.contrib.auth.models import User

SUPERUSER_USERNAME = "admin"
SUPERUSER_EMAIL = "admin@admin.co.in"
SUPERUSER_PASSWORD = "admin"

if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
    User.objects.create_superuser(
        SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD
    )