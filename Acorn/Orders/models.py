from django.db import models
from django.conf import settings

from Account.models import UserAddress
from Inventory.models import ProductInventory
from Delivery.models import DeliveryOptions
from Payment.models import PaymentSelections



class Order(models.Model):
    
    class Meta:
        ordering = ("-created",)

    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="user_orders")
    address = models.ForeignKey(UserAddress, on_delete=models.PROTECT, related_name="order_addresses")
    delivery_option = models.ForeignKey(DeliveryOptions, on_delete=models.PROTECT, related_name="order_delivery_option")
    payment_method = models.ForeignKey(PaymentSelections, on_delete=models.PROTECT, related_name="order_payment_method")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    billing_status = models.BooleanField(default=False)
    order_key = models.CharField(max_length=200, null=True, blank=True)



class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(ProductInventory, on_delete=models.PROTECT, related_name="order_items")
    
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    