from django.db import models
from django.utils.translation import gettext_lazy as _



class DeliveryOptions(models.Model):
    """
    The Delivery methods table contining all delivery
    """

    class Meta:
        verbose_name = _("Delivery option")
        verbose_name_plural = _("Delivery options")
        ordering = ("order",)


    DELIVERY_CHOICES = [
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
    ]

    delivery_name = models.CharField(
        verbose_name=_("delivery name"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_price = models.DecimalField(
        verbose_name=_("delivery price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    delivery_method = models.CharField(
        choices=DELIVERY_CHOICES,
        verbose_name=_("delivery method"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_timeframe = models.CharField(
        verbose_name=_("delivery timeframe"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_window = models.CharField(
        verbose_name=_("delivery window"),
        help_text=_("Required"),
        max_length=255,
    )
    order = models.IntegerField(
        verbose_name=_("list order"), 
        help_text=_("Required"),
        default=0
    )
    is_active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return self.delivery_name