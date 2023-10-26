from rest_framework import mixins, viewsets, permissions
from rest_framework.response import Response

from Inventory.models import Product, ProductInventory
from .serializers import ProductSerializer, ProductInventorySerializer



class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


    def retrieve(self, request, slug=None):
        queryset = Product.objects.filter(category__slug=slug)[:10]
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    


class ProductInventoryViewSet(mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    queryset = ProductInventory.objects.all()


    def list(self, request, slug=None):
        queryset = ProductInventory.objects.filter(
            product__category__slug=slug
        ).filter(
            is_default=True
        )[:10]
        serializer = ProductInventorySerializer(queryset, context={"request": request}, many=True)
        return Response(serializer.data)