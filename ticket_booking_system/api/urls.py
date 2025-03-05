from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, OrderViewSet, EventViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'events', EventViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
