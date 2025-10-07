
from django.core.asgi import get_asgi_application
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import monitoringapp.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitoring.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
      URLRouter(monitoringapp.routing.websocket_urlpatterns)
  )
})
