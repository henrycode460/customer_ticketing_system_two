
from django.urls import path
from . import consumer
from .consumer import TicketConsumer

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<ticket>\d+)/$', TicketConsumer.as_asgi()),
#    url(r'^ws/chat/(?P<ticket>\d+)/$', TicketConsumer.as_asgi()),
   path('ws/chat/<int:pk>/', consumer.TicketConsumer.as_asgi()),
]
