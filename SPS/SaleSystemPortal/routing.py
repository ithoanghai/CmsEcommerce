from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from creme.friends import routing as friends_routing
from creme.notifications import routing as notifications_routing
from creme.communications import routing as communications_routing


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            friends_routing.websocket_urlpatterns + notifications_routing.websocket_urlpatterns + communications_routing.websocket_urlpatterns
        )),
})