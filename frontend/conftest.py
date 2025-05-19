import os

import django

# Set the Django settings module path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

# Initialize Django
django.setup()
