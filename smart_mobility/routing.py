from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/transport/(?P<route_id>\w+)/$', consumers.TransportConsumer.as_asgi()),
    re_path(r'ws/traffic/$', consumers.TrafficConsumer.as_asgi()),
] 