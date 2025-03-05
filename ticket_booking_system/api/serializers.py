from rest_framework import serializers
from .models import Ticket, Event, Order

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'owner', 'order', 'created_at']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'location', 'max_tickets']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status']