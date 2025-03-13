from django.contrib import admin
from django.urls import path
from api.admin_views import stats_dashboard
from api.models import User, Event, Order, Ticket

class CustomAdminSite(admin.AdminSite):
    site_header = "Ticket Booking Admin"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('stats-dashboard/', self.admin_view(stats_dashboard), name='stats-dashboard'),
        ]
        return custom_urls + urls

admin_site = CustomAdminSite(name='myadmin')

admin_site.register(User)
admin_site.register(Event)
admin_site.register(Order)
admin_site.register(Ticket)
