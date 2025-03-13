from django.db.models import Count, Q
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from api.models import Event, Order, Ticket, User

@staff_member_required
def stats_dashboard(request):

    events = Event.objects.annotate(ticket_count=Count('tickets'))
    
    paid_orders = Order.objects.filter(status='successful').aggregate(paid_tickets=Count('tickets'))
    unpaid_orders = Order.objects.filter(status='failed').aggregate(unpaid_tickets=Count('tickets'))
    
    top_users = User.objects.annotate(ticket_count=Count('tickets')).order_by('-ticket_count')[:10]

    context = {
        'events': events,
        'paid_orders': paid_orders,
        'unpaid_orders': unpaid_orders,
        'top_users': top_users,
    }
    return render(request, 'admin/stats_dashboard.html', context)
