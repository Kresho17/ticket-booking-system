import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Event, User


@pytest.mark.django_db
class TestEventListView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('event_list')
        Event.objects.create(
            name="Event 1",
            description="Desc 1",
            date="2025-01-01T12:00:00Z",
            location="Location 1",
            max_tickets=50
        )
        Event.objects.create(
            name="Event 2",
            description="Desc 2",
            date="2025-01-02T12:00:00Z",
            location="Location 2",
            max_tickets=100
        )

        self.data = {
            "name": "Unauthorized Event",
            "description": "Should fail",
            "date": "2025-01-03T12:00:00Z",
            "location": "Location X",
            "max_tickets": 70
        }

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword123",
        )


    def test_get_events(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_post_event_unauthenticated(self):
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code in [401, 403]

    def test_post_event_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code in [401, 403]

    def test_post_event_authenticated_isAdmin(self):
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="securepass123",
        )
        self.client.force_authenticate(user=admin_user)
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code == 201

    def test_patch_event(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, self.data, format="json")
        assert response.status_code == 405

    def test_put_event(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, self.data, format="json")
        assert response.status_code == 405

    def test_delete_event(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, self.data, format="json")
        assert response.status_code == 405

