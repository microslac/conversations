"""
ASGI config for api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from starlette.applications import Starlette
from starlette.routing import Mount

from api.lifespan import lifespan_context

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

application = Starlette(routes=[Mount("/", get_asgi_application())], lifespan=lifespan_context)
