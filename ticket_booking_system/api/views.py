import logging
import random
import requests
from django.conf import settings
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from .models import Ticket, Event, Order
from .serializers import EventSerializer, OrderSerializer, UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from api.paginaion import CustomPagination


logger = logging.getLogger("Payments_logger")


# EventList responsible for Listing Event and creating a new event
class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = CustomPagination

    # Set Permissions for different requests
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAdminUser(), IsAuthenticated()]
        return super().get_permissions()


# LogoutView responsible for logut the user (blacklisting tokens)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh', None)
            if refresh_token is None:
                return Response({'detail': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'detail': 'Successfully logged out and token blacklisted'}, status=status.HTTP_205_RESET_CONTENT)
        
        except TokenError:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        

# UserRegisterView responsible for user registration
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserRegistrationSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# EventChangeView responsible for CRUD operation for an event
class EventChangeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    

class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data = request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# DeleteOrder responsible for canceling orders [Admmin, User who requested it] 
class DeleteOrder(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        try:
            if request.user.is_staff:
                order = Order.objects.get(id=id)
            else:
                order = Order.objects.get(id=id, user=request.user)

            order.status = 'deleted'
            order.save()

            tickets = Ticket.objects.filter(order=order)
            tickets.delete()

            return Response({"detail": "Order status updated to 'deleted'"}, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"detail": "Order not found or not authorized to update this order."}, status=status.HTTP_404_NOT_FOUND)


# SimulatePayment responsible for payment service provider simulation
class SimulatePayment(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        # Random success or failure simulation
        success = random.choice([True, False])

        if success:
            return Response(
                {"message": "Payment was successful.", "status": "successful"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Payment failed.", "status": "failed"},
                status=status.HTTP_400_BAD_REQUEST
            )


# ProcessPayment responsible for ticket payment
class ProcessPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            order = Order.objects.get(id=id)

            # The payment has either failed or been made.
            if order.status != 'pending':
                return Response(
                    {"message": f"Order {id} payment cannot be processed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Simulate the payment process
            payment_response = requests.get(
                f"{settings.BASE_URL}/api/simulate-payment/"
            )

            if payment_response.status_code == 200:
                order.status = 'successful'
                order.save()
                return Response(
                    {"message": f"Order {id} payment was successful."},
                    status=status.HTTP_200_OK
                )
            else:
                # Continues to wait for successful payment
                order.status = 'pending'
                order.save()
                return Response(
                    {"message": f"Order {id} payment failed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Order.DoesNotExist:
            return Response({"error": f"Order {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        except requests.RequestException as e:
            return Response(
                {"error": f"Payment request failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )