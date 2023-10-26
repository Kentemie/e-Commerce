from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from DRF.views import ProductViewSet, ProductInventoryViewSet

from Search.views import SearchProductInventory


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename="products")
router.register(r'inventory/(?P<slug>[^/.]+)', ProductInventoryViewSet, basename="inventory")


urlpatterns = [
    path('', include("Demo.urls", namespace="demo")),
    path('cart/', include("Cart.urls", namespace="cart")),
    path('account/', include("Account.urls", namespace="account")),
    path('payment/', include("Payment.urls", namespace="payment")),
    path('orders/', include("Orders.urls", namespace="orders")),
    path('delivery/', include("Delivery.urls", namespace="delivery")),
    path('admin/', admin.site.urls),

    # API and SEO
    path('api/', include(router.urls)),
    path('search/<str:query>/', SearchProductInventory.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
