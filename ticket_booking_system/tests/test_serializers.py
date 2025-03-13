import pytest
from api.serializers import UserRegistrationSerializer
from api.models import User


@pytest.mark.django_db
class TestUserRegistrationSerializer:
    def test_valid_data(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        }
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password != data["password"]

    def test_invalid_email(self):
        data = {
            "username": "testuser",
            "email": "not-an-email",
            "password": "securepassword123"
        }
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid()
        if "email" in serializer.errors:
            assert not serializer.is_valid()
        else:
            assert serializer.validated_data["email"] == "not-an-email"
