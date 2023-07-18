"""
ASGI config for {{ cookiecutter.project_name }} project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "{{ cookiecutter.project_slug }}"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_slug }}.settings")

application = get_asgi_application()
