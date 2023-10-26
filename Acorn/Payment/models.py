from django.db import models
from django.utils.translation import gettext_lazy as _



class PaymentSelections(models.Model):
    """
    Store payment options
    """

    class Meta:
        verbose_name = _("Payment selection")
        verbose_name_plural = _("Payment selections")


    PAYMENT_CHOICES = [
        ("S", "Stripe"),
        ("P", "PayPal"),
    ]

    name = models.CharField(
        choices=PAYMENT_CHOICES,
        verbose_name=_("name"),
        help_text=_("Required"),
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name