from django.contrib.auth.models import AbstractUser
from django.db import models
# TODO: Change Cascade to Protected or Use a new table for deleted users


class User(AbstractUser):
    pass


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    max_tickets = models.PositiveIntegerField()

    # TODO: Implement the counting of the available tickets
    def available_tickets(self):
        pass

    def sold_tickets(self):
        pass

    def __str__(self):
        return self.name


class Order(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('deleted', 'Deleted')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.get_status_display()}"


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id} for {self.event.name} - {self.owner.username}"
