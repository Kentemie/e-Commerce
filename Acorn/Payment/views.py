import stripe
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.conf import settings
from django.core.serializers import serialize

from Cart.cart import Cart
from Orders.views import payment_confirmation

from .models import PaymentSelections
from .forms import UserForm

from Account.forms import UserAddressForm
from Account.models import UserAddress



@login_required
def checkout(request):

    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    # Receive active payment options
    payment_options = PaymentSelections.objects.filter(is_active=True)

    if request.method == "POST": 
        user_form = UserForm(request.POST, instance=request.user)
        address_form = UserAddressForm(request.POST)

        if user_form.is_valid():
            # Save this info for I do not now know what yet
            first_name = user_form.cleaned_data.get("first_name")
            last_name = user_form.cleaned_data.get("last_name")

            if 'save_information' in request.POST:
                request.user.delivery_info = True
                request.user.save()

            if 'shipping_address' in request.POST:
                # Getting the user's primary address
                user_main_address = UserAddress.objects.get(user=request.user, is_main=True)
                serialized_data = serialize('python', [user_main_address])[0]['fields']

                return JsonResponse({
                    "success": "Data is valid",
                    "first_name": first_name,
                    "last_name": last_name,
                    "address_data": serialized_data,
                    "payment_method": request.POST.get("payment_method")
                })
            
            else:
                if address_form.is_valid():
                    address_data = json.dumps(address_form.cleaned_data)

                    return JsonResponse({
                        "success": "Data is valid",
                        "first_name": first_name,
                        "last_name": last_name,
                        "address_data": address_data,
                        "payment_method": request.POST.get("payment_method")
                    })

                else:
                    # Errors in address form
                    return JsonResponse({
                        "address_form_errors": address_form.errors,
                    })

        else:
            # Errors in the user form
            return JsonResponse({
                "user_form_errors": user_form.errors,
            })

    else:
        # Initializing forms for user and address
        user_form = UserForm()
        address_form = UserAddressForm()

        user_billing_address = UserAddress.objects.filter(user=request.user, is_main=True)

        if request.user.delivery_info == True and user_billing_address.exists():

            user_form = UserForm(instance=request.user)
            address_form = UserAddressForm(instance=user_billing_address.first())


    return render(request, 'payment/checkout.html', {
        "payment_options": payment_options,
        "user_form": user_form,
        "address_form": address_form,
    })

@login_required 
def check_address(request):
    return JsonResponse({
        "has_billing_address": UserAddress.objects.filter(user=request.user, is_main=True).exists()
    })

# <-- Stripe -->

@login_required
def stripe_payment(request):
    if request.POST.get("action") == "post":
        basket = Cart(request)
        total = int(str(basket.get_total_price()).replace('.', '') + '0')

        stripe.api_key = settings.SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='gbp',
            metadata={
                'userid': request.user.id
            }
        )
        
        return JsonResponse({
            'client_secret': intent.client_secret
        })
    

class Error(TemplateView):
    template_name = 'payment/stripe/error.html'


def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/stripe/orderplaced.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)
    
    # Handle the event
    if event.type == "payment_intent.succeeded":
        payment_confirmation(event.data.object.client_secret)
    else:
        print(f"Unhandled event type {event.type}")
    
    return HttpResponse(status=200)

# <-- _ -->