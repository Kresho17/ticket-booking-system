from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Order


@shared_task
def update_order_status_to_failed(order_id):
    try:
        order = Order.objects.get(id=order_id)
    
        # Check if the status is still 'pending'
        if order.status == 'pending':
            order.status = 'failed'
            order.save()

            # Delete related tickets
            tickets = order.tickets.all()

            deleted_count, _ = tickets.delete()

            return f"Order {order_id} status updated to 'failed' and tickets deleted."
        else:
            return f"Order {order_id} status not updated (already changed)."
    except Order.DoesNotExist:
        return f"Order {order_id} does not exist."