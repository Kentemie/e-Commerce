from django.urls import path

from .views import (
    checkout,
    order_placed,
    stripe_webhook,
    stripe_payment,
    check_address,
)

app_name = "payment"

urlpatterns = [
    path('', checkout, name="checkout"),
    path('order_placed/', order_placed, name="order_placed"),
    path('webhook/', stripe_webhook),
    path('stripe_payment/', stripe_payment, name="stripe_payment"),
    path('check_address/', check_address, name="check_address"),
]
