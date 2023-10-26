from django.urls import path

from .views import (
    delivery_choices,
    cart_update_delivery,
    delivery_address,
    payment_selection,
)

app_name = "delivery"

urlpatterns = [
    path("delivery_choices/", delivery_choices, name="delivery_choices"),
    path("cart_update_delivery/", cart_update_delivery, name="cart_update_delivery"),
    path("delivery_address/", delivery_address, name="delivery_address"),
    path("payment_selection/", payment_selection, name="payment_selection"),
]