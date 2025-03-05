""" from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, OrderViewSet, EventList

router = DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'events', EventList)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
 """

from django.urls import path
from .views import EventList

urlpatterns = [
    path('events/', EventList.as_view(), name='event-list'),
]