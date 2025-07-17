from django.urls import path

from apps.auto_salon_listings.consumers import AutoSalonListingConsumer

websocket_urlpatterns = [
    path('', AutoSalonListingConsumer.as_asgi(), name='websocket_auto_salon_listings'),
]