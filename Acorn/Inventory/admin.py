from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product, ProductInventory



class InventoryAdmin(admin.ModelAdmin):

    list_display = ["product", "store_price"]



admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)
admin.site.register(Product)
admin.site.register(ProductInventory, InventoryAdmin)