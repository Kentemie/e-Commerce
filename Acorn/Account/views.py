from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string

from .models import UserModel, UserAddress
from .forms import (
    RegistrationForm,
    UserEditForm,
    UserAddressForm
)
from .tokens import account_activation_token

from Orders.views import user_orders
from Inventory.models import ProductInventory


def account_register(request):

    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)

        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your account.'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject=subject, message=message)

            return render(request, 'account/registration/register_email_confirm.html', {'form': registerForm})
        
    registerForm = RegistrationForm()

    return render(request, 'account/registration/register.html', {'form': registerForm})

def account_activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
    

# Dashboard

@login_required
def dashboard(request):
    return render(request, 'account/dashboard/dashboard.html')

@login_required
def orders(request):
    orders = user_orders(request)
    return render(request, 'account/dashboard/orders.html', {'orders': orders})

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'account/dashboard/edit_details.html', {'user_form': user_form})

@login_required
def delete_user(request):
    user = UserModel.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


# Addresses 

@login_required
def view_address(request):

    addresses = UserAddress.objects.filter(user=request.user.id)

    return render(request, 'account/dashboard/addresses.html', {'addresses': addresses})

@login_required
def add_address(request):

    if request.method == "POST":
        address_form = UserAddressForm(request.POST)

        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('account:addresses')

    address_form = UserAddressForm()

    return render(request, 'account/dashboard/edit_addresses.html', {'form': address_form})

@login_required
def edit_address(request, id):
    address = UserAddress.objects.get(pk=id, user=request.user)

    if request.method == "POST":
        address_form = UserAddressForm(instance=address, data=request.POST)

        if address_form.is_valid(): 
            address_form.save()
            return redirect('account:addresses')
    else:
        address_form = UserAddressForm(instance=address)

    return render(request, 'account/dashboard/edit_addresses.html', {'form': address_form})

@login_required
def delete_address(request):
    if request.POST.get("action") == "delete":
        UserAddress.objects.get(pk=request.POST.get("address_id"), user=request.user).delete()
        return JsonResponse({})

@login_required
def set_default(request, id):

    UserAddress.objects.filter(user=request.user, is_main=True).update(is_main=False)
    UserAddress.objects.filter(pk=id, user=request.user).update(is_main=True)

    if "delivery_address" in request.META.get("HTTP_REFERER"):
        return redirect('payment:delivery_address')

    return redirect('account:addresses')


# User wishlist

@login_required
def wishlist(request):
    products = ProductInventory.objects.filter(users_wishlist=request.user)
    return render(request, "account/dashboard/user_wish_list.html", {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(ProductInventory, id=id)

    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.product.name + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.product.name + " to your WishList")

    return HttpResponseRedirect(request.META["HTTP_REFERER"])