from django.urls import path

from .views import (
    default_products,
    products_by_category,
    product_detail,
)

app_name = "demo"

urlpatterns = [
    path('', default_products, name="default_products"),
    path('product-by-category/<slug:category>/', products_by_category, name="products_by_category"),
    path('product-detail/<slug:slug>', product_detail, name="product_detail"),
]
