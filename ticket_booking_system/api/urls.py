from django.urls import path
from .views import EventChangeView, EventList, LogoutView, UserRegisterView, CreateOrder
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('events/', EventList.as_view(), name='event_list'),
    path('events/<int:id>/', EventChangeView.as_view(), name='event_change'),
    path("orders/", CreateOrder.as_view(), name="order_create"),
]