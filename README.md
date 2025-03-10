# Ticket Booking System

This is a ticket booking system built with Django, Redis as a message broker, and Celery for background tasks.

## Getting Started

### 1. Clone the Project

First, clone the project from GitHub:

```bash
git clone https://github.com/Kresho17/ticket-booking-system.git
cd ticket-booking-system
```

### 2. Create the .env File

The project requires a .env file for environment variables. To create this file:
1. Copy the template.env file to a new file named .env:

```bash
cp template.env .env
```

2. Open the .env file and fill in the necessary values for your local environment (e.g., database credentials, API keys, etc.).


### 3. Run Docker Compose

```bash
docker-compose up --build
```

This will create and start the following containers:
- Django Application
- Redis (Message Broker)
- Celery (Background tasks)

### 4. Access the Application

```bash
http://localhost:8000
```

### 5. Admin Panel

To access the Django admin panel, create a superuser by running the following command:

```bash
docker-compose exec web python manage.py createsuperuser
```
After creating the superuser, you can access the admin panel at:
```bash
http://localhost:8000/admin
```

---

## API Views Documentation

### 1. `EventList` - List and Create Events
- **URL:** `/api/events/`
- **Methods:** `GET`, `POST`
- **Permissions:**
  - `GET`: Open to all users (`AllowAny`).
  - `POST`: Accessible only to authenticated admin users (`IsAdminUser`, `IsAuthenticated`).
  
This view lists all events and allows the creation of new events. 

---

### 2. `LogoutView` - Logout and Blacklist Token
- **URL:** `/api/logout/`
- **Method:** `POST`
- **Permissions:** `IsAuthenticated`
  
This view allows users to log out and blacklist the refresh token.

#### Workflow:
- The refresh token is required to log out and invalidate the token for further use.

---

### 3. `UserRegisterView` - User Registration
- **URL:** `/api/register/`
- **Method:** `POST`
- **Permissions:** `AllowAny`
  
This view allows new users to register by providing necessary details like username, email, and password.

---

### 4. `EventChangeView` - Update or Delete Events
- **URL:** `/api/events/{id}/`
- **Methods:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Permissions:**
  - `GET`: Open to all users (`AllowAny`).
  - `PUT`, `PATCH`, `DELETE`: Accessible only to admin users (`IsAdminUser`).
  
This view handles CRUD operations (Create, Retrieve, Update, Delete) on events. Only admins can modify or delete events.

---

### 5. `CreateOrder` - Create an Order
- **URL:** `/api/orders/`
- **Method:** `POST`
- **Permissions:** `IsAuthenticated`
  
This view allows authenticated users to create a new order for a ticket. The user must be logged in to place an order.

---

### 6. `DeleteOrder` - Delete or Cancel an Order
- **URL:** `/api/orders/{id}/`
- **Method:** `PATCH`
- **Permissions:** `IsAuthenticated`
  
This view allows users (or admins) to cancel or delete an order. Admin users can delete any order, while regular users can only delete their own orders.

---

### 7. `SimulatePayment` - Simulate Payment Service
- **URL:** `/api/simulate-payment/`
- **Method:** `GET`
- **Permissions:** `AllowAny`
  
This view simulates a payment process, either successful or failed, by randomly selecting one of the two options. No authentication is required for this endpoint.

#### Response:
- **200 OK**: Payment was successful.
- **400 Bad Request**: Payment failed.

---

### 8. `ProcessPayment` - Process Payment for Order
- **URL:** `/api/process-payment/{id}/`
- **Method:** `POST`
- **Permissions:** `IsAuthenticated`
  
This view allows authenticated users to process the payment for a given order. The order status is updated based on the result of the payment simulation.

#### Workflow:
- The order status is checked. If the status is not `pending`, the payment cannot be processed.
- A GET request is made to the `/api/simulate-payment/` endpoint to simulate the payment.
- Based on the payment simulation result, the order status is updated to either `successful` or remains `pending`.

#### Response:
- **200 OK**: Payment successful, order status updated.
- **400 Bad Request**: Payment failed, order status remains `pending`.
- **404 Not Found**: Order not found.
- **500 Internal Server Error**: If the payment request fails.
