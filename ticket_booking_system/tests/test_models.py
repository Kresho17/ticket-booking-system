import pytest
from api.models import Event, Order, User, Ticket


@pytest.mark.django_db
class TestEventModel():
    def setup_method(self):
        
        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass"
        )

        # Create test Event
        self.event = Event.objects.create(
            name = "Test Event",
            description = "Test Description",
            date = "2025-01-01T12:00:00Z",
            location = "Test Location",
            max_tickets = 100,
        )

        # Create three Order: one with pending and the other with successful, and the last one with failed status
        self.order_pending = Order.objects.create(
            user=self.user,
            status="pending",
        )
        self.order_successful = Order.objects.create(
            user=self.user,
            status="successful",
        )
        self.order_failed = Order.objects.create(
            user=self.user,
            status="failed",
        )

        # Create tickets for each order
        Ticket.objects.create(
            event=self.event,
            owner=self.user,
            order=self.order_pending
        )
        Ticket.objects.create(
            event=self.event,
            owner=self.user,
            order=self.order_successful
        )
        Ticket.objects.create(
            event=self.event,
            owner=self.user,
            order=self.order_failed
        )


    def test_available_tickets(self):
        # event.max_tickets 100, we have two ticket (pending, successfull) and one failed ticket which is not count
        assert self.event.available_tickets() == 98

    def test_sold_tickets(self):
        # event.max_tickets 100, we have two ticket (pending, successfull) and one failed ticket which is not count
        assert self.event.sold_tickets() == 2