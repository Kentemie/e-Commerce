from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from Inventory.models import ProductInventory



@registry.register_document
class ProductInventoryDocument(Document):

    class Index:
        name = "product_inventory"

    class Django:
        model = ProductInventory

        fields = [
            "id",
            "sku",
            "store_price",
            "is_default",
        ]


    product = fields.ObjectField(
        properties = {
            "name": fields.TextField(),
            "web_id": fields.TextField()
        }
    )

    brand = fields.ObjectField(
        properties = {
            "name": fields.TextField()
        }
    )