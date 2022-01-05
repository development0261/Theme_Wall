"""
ASGI config for themenswall project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django

from channels.routing import get_default_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'themenswall.settings')
django.setup()
application = get_default_application()


# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from django.core.asgi import get_asgi_application
# import feed
# from channels.auth import AuthMiddlewareStack
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'themenswall.settings')

# application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
#   "websocket": AuthMiddlewareStack(
#         URLRouter(
#             feed.routing.websocket_urlpatterns
#         )
#     ),
# })