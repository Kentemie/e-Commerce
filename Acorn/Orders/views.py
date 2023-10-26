from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from Cart.cart import Cart
from Account.models import UserAddress
from Delivery.models import DeliveryOptions
from Payment.models import PaymentSelections

from .models import Order, OrderItem


User = get_user_model()


def add(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        user = User.objects.get(id=request.user.id)
        address, _ = UserAddress.objects.get_or_create(
            user=user,
            country=request.POST.get("address_data[country]"),
            city=request.POST.get("address_data[city]"),
            postal_code=request.POST.get("address_data[postal_code]"),
            address_line_1=request.POST.get("address_data[address_line_1]"),
            address_line_2=request.POST.get("address_data[address_line_2]"),
            phone_number_1=request.POST.get("address_data[phone_number_1]"),
        )
        delivery_option = get_object_or_404(DeliveryOptions, pk=request.session["purchase"]["delivery_id"])
        payment_method = PaymentSelections.objects.get(name=request.POST.get("payment_method"))

        order_key = request.POST.get("order_key")
        cart_total_price = cart.get_total_price()

        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user=user, 
                address=address,
                delivery_option=delivery_option,
                payment_method=payment_method,
                
                total_price=cart_total_price, 
                order_key=order_key
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order, 
                    product=item["product"], 
                    price=item["store_price"],
                    quantity=item["quantity"]
                )
        response = JsonResponse({
            "success": "Some gibberish",
        })

        return response
    
def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)

def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user=user_id).filter(billing_status=True)
    return orders