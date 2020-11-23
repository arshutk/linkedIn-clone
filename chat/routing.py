from django.urls import path

from chat.consumers import ChatConsumer

websocket_urlpatterns = [
  
    # path(r'^ws/chat/(?P<room_name>[^/]+)/(?P<auth>[^/]+)/$', ChatConsumer)
    path('ws/chat/<int:sender_id>/<int:receiver_id>/', ChatConsumer.as_asgi())
    
]