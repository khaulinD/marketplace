
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from webchat.middleware import JWTAuthMiddleWare

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.settings')

django_application = get_asgi_application()

from . import urls
# from webchat.middleware import JWTAuthMiddleWare # noqa isort:skip
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleWare(URLRouter(urls.websocket_urlpatterns))
})