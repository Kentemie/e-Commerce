from django.shortcuts import render

from Inventory.models import Product, ProductInventory


def default_products(request):
    products = Product.objects.filter(
        product__is_default=True
    )
    # .values(
        # "name", "slug", "product__media_product_inventory__img_url", "product__store_price"
    # )


    return render(request, "demo/home.html", {"products": products})


def products_by_category(request, category):
    products = Product.objects.filter(
        category__slug=category, product__is_default=True
    )
    
    return render(request, "products/products_by_category.html", {"products": products})


def product_detail(request, slug):
    product = ProductInventory.objects.get(
        product__slug=slug, 
        is_default=True
    )

    if request.user.is_authenticated:
        in_the_wishlist = ProductInventory.objects.filter(product__slug=slug, users_wishlist=request.user).exists()
        return render(request, "products/detail.html", {"product": product, "in_the_wishlist": in_the_wishlist})

    return render(request, "products/detail.html", {"product": product})