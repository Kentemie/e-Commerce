from django.urls import path

from .views import summary, update

app_name = "cart"

urlpatterns = [
    path('', summary, name="summary"),
    path('update/', update, name="update"),
]
