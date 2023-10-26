from rest_framework import serializers

from Inventory.models import (
    Product, 
    Brand, 
    ProductAttributeValue, 
    ProductInventory, 
    Media,
    Category,
    ProductType
)
    


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name"]



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        # fields = ["web_id", "slug", "name", "description", "category"]
        fields = ["name", "web_id"]
        read_only = True 
        editable = False


    # category = CategorySerializer(many=True)



class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand 
        fields = ["name"]



class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ["name"]



class ProductAttributeValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttributeValue
        exclude = ["id"]
        depth = 2



class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ["img_url", "alt_text"]

    
    img_url = serializers.SerializerMethodField()


    def get_img_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.image.url)



class ProductInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInventory
        fields = [
            "sku",
            "image",
            "price",
            "is_default",
            "product",
            "brand",
            "type",
            "attributes",
        ]
        read_only = True 


    image = MediaSerializer(source="media_product_inventory", many=True, read_only=True)
    price = serializers.DecimalField(source="retail_price", max_digits=5, decimal_places=2)
    product = ProductSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    type = ProductTypeSerializer(source="product_type", read_only=True)
    attributes = ProductAttributeValueSerializer(source="product_attribute_values", many=True, read_only=True)



class ProductInventorySearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "sku",
            "store_price",
            "is_default",
            "product",
            "brand"
        ]


    product = ProductSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
