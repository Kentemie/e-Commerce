from django.urls import path

from .views import (
    add,
)

app_name = "orders"

urlpatterns = [
    path('add/', add, name="add"),
]