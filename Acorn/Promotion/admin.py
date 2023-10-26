from django.contrib import admin

from .models import Promotion, Coupon, PromotionType
from .tasks import promotion_prices, promotion_management



class ProductOnPromotion(admin.StackedInline):

    model = Promotion.products_on_promotion.through
    extra = 3
    raw_id_fields = ["product_inventory"]



class ProductInventoryList(admin.ModelAdmin):

    model = Promotion
    inlines = [ProductOnPromotion]
    list_display = [
        "name",
        "is_active",
        "promotion_start",
        "promotion_end"
    ]


    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        promotion_prices.delay(obj.promotion_reduction, obj.id)
        promotion_management.delay()



admin.site.register(Promotion, ProductInventoryList)
admin.site.register(Coupon)
admin.site.register(PromotionType)