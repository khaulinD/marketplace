from django.urls import path

from webchat.consumer import WebChatConsumer

websocket_urlpatterns_webchat = [
    path("chat/<int:id>", WebChatConsumer.as_asgi())
]