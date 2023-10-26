from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .cart import Cart

from Inventory.models import ProductInventory

from Delivery.models import DeliveryOptions


def summary(request):
    delivery_options = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "cart/summary.html", {"delivery_options": delivery_options})


def update(request):
    cart = Cart(request)
    product_id = request.POST.get("product_id")

    if request.POST.get("action") == "add":
        product_qty = request.POST.get("product_qty")
        
        product = get_object_or_404(ProductInventory, id=product_id)

        cart.add(product=product, product_qty=product_qty)
        
        response = JsonResponse({"qty": cart.__len__()})
        return response
    
    elif request.POST.get("action") == "delete":
        cart.delete(product=product_id)

        response = JsonResponse({
            "qty": cart.__len__(),
            "new_sub_total": cart.get_subtotal_price(),
            "new_total": cart.get_total_price()
        })

        return response
    
    elif request.POST.get("action") == "update":
        product_qty = request.POST.get("product_qty")

        cart.update(product_id=product_id, product_qty=product_qty)

        response = JsonResponse({
            "qty": cart.__len__(),
            "new_sub_total": cart.get_subtotal_price(),
            "new_total": cart.get_total_price()
        })

        return response
    