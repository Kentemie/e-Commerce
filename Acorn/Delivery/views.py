from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import JsonResponse, HttpResponseRedirect

from .models import DeliveryOptions

from Cart.cart import Cart

from Account.models import UserAddress


@login_required
def delivery_choices(request):
    delivery_options = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "delivery/delivery_choices.html", {"delivery_options": delivery_options})

@login_required
def cart_update_delivery(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        delivery_option = request.POST.get("delivery_option")
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = cart.cart_update_delivery(float(delivery_type.delivery_price))

        session = request.session

        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        return JsonResponse({"total": updated_total_price, 
                             "delivery_price": delivery_type.delivery_price, 
                             "delivery_name": delivery_type.delivery_name})
    
@login_required
def delivery_address(request):
    session = request.session

    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = UserAddress.objects.filter(user=request.user).order_by("-is_main")

    if not addresses:
        return redirect('account:add_address')

    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True

    return render(request, "delivery/delivery_address.html", {"addresses": addresses})

@login_required
def payment_selection(request):

    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "delivery/payment_selection.html")