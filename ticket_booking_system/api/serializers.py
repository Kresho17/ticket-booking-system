from rest_framework import serializers
from .models import Ticket, Event, Order, User
from .tasks import update_order_status_to_failed


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
class TicketSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'owner', 'order', 'created_at']
        read_only_fields = ['created_at', 'order']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'location', 'max_tickets', 'available_tickets', 'sold_tickets']

    def get_available_tickets(self, obj):
        return obj.available_tickets()

    def get_sold_tickets(self, obj):
        return obj.sold_tickets()

class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'tickets']

    def validate(self, data):
        tickets_data = data.get('tickets', [])
        
        # Stores how many tickets the user requests for each event
        event_request_count = {}

        for ticket in tickets_data:
            event_id = ticket['event'].id

            if event_id in event_request_count:
                event_request_count[event_id] += 1
            else:
                event_request_count[event_id] = 1

        # Summary of tickets already purchased by the user
        user = self.context['request'].user
        user_event_ticket_count = {}

        # Query the tickets already purchased by the user and count them
        for ticket in Ticket.objects.filter(owner=user):
            event_id = ticket.event.id
            if event_id not in user_event_ticket_count:
                user_event_ticket_count[event_id] = 0
            user_event_ticket_count[event_id] += 1

        # Check if the user cannot request more than 5 tickets for an event
        for event_id, requested_count in event_request_count.items():
 
            current_event_ticket_count = user_event_ticket_count.get(event_id, 0)
            
            total_ticket_count = current_event_ticket_count + requested_count

            if total_ticket_count > 5:
                raise serializers.ValidationError(f"You cannot buy more than 5 tickets for event with ID {event_id}")
            
            # Check if there are enough tickets available
            event = Event.objects.get(id=event_id)
            if requested_count > event.available_tickets():
                raise serializers.ValidationError(f"Not enough available tickets for event: {event.name}")

        return data

    
    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets', [])
        order = Order.objects.create(**validated_data)

        # Start the Celery task to update the status in 15 minutes.
        update_order_status_to_failed.apply_async(args=[order.id], countdown=15*60)

        for ticket_data in tickets_data:
            ticket_data['owner'] = validated_data['user']
            Ticket.objects.create(order=order, **ticket_data)

        return order