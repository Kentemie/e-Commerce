from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from Inventory.models import ProductInventory

from decimal import Decimal



class PromotionType(models.Model):

    name = models.CharField(
        max_length=255
    )


    def __str__(self):
        return self.name
    


class Coupon(models.Model):

    name = models.CharField(
        max_length=255
    )

    coupon_code = models.CharField(
        max_length=20
    )



class Promotion(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    promotion_reduction = models.IntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=False
    )

    is_scheduled = models.BooleanField(
        default=False
    )

    promotion_start = models.DateField()

    promotion_end = models.DateField()

    products_on_promotion = models.ManyToManyField(
        ProductInventory,
        related_name="products_on_promotion",
        through="ProductsOnPromotion"
    )

    promotion_type = models.ForeignKey(
        PromotionType,
        related_name="promotion_type",
        on_delete=models.PROTECT
    )

    coupon = models.ForeignKey(
        Coupon,
        related_name="coupon",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )


    def clean(self):
        if self.promotion_start > self.promotion_end:
            raise ValidationError(_("You have entered incorrect start and end dates for the promotion!"))
    
    def __str__(self):
        return self.name
    


class ProductsOnPromotion(models.Model):

    class Meta:
        unique_together = (("product_inventory", "promotion"))


    product_inventory = models.ForeignKey(
        ProductInventory,
        related_name="product_inventory_on_promotion",
        on_delete=models.PROTECT
    )

    promotion = models.ForeignKey(
        Promotion,
        related_name="promotion",
        on_delete=models.PROTECT
    )

    promotion_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    price_override = models.BooleanField(
        default=False
    )