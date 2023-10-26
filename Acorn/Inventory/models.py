from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey

from decimal import Decimal

class Category(MPTTModel):

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("Product categories")

    class MPTTMeta:
        order_insertion_by = ["name"]


    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Category name"),
    )
    
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name=_("Category safe URL"),
    )
    
    is_active = models.BooleanField(
        default=False
    )

    parent = TreeForeignKey(
        "self", 
        on_delete=models.PROTECT,
        null=True, 
        blank=True,
        related_name="children"
    )
    
    
    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse("demo:products_by_category", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
    


class Product(models.Model):

    web_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Product website ID"),
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Product name"),
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_("Product safe URL"),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("Product description"),
    )

    category = models.ForeignKey(
        Category,
        related_name="category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Date product created"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date product last updated"),
    )


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


    
class ProductAttribute(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Product attribute name"),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("Product attribute description"),
    )


    def __str__(self):
        return self.name



class ProductType(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Type of product"),
    )

    product_type_attributes = models.ManyToManyField(
        ProductAttribute,
        related_name="product_type_attributes",
        through="ProductTypeAttribute"
    )
    

    def __str__(self):
        return self.name
    


class Brand(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Brand name"),
    )
    

    def __str__(self):
        return self.name
    


class ProductAttributeValue(models.Model):

    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_attribute",
        on_delete=models.PROTECT
    )

    attribute_value = models.CharField(
        max_length=255,
        verbose_name=_("Attribute value"),
    )

    
    def __str__(self):
        return f"{self.product_attribute.name} - {self.attribute_value}"



class ProductInventory(models.Model):

    class Meta:
        verbose_name = _("Product inventory")
        verbose_name_plural = _("Product inventories")


    sku = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Stock keeping unit"),
    )

    upc = models.CharField(
        max_length=12,
        unique=True,
        verbose_name=_("Universal product code"),
    )

    product_type = models.ForeignKey(
        ProductType, 
        related_name="product_type",
        on_delete=models.PROTECT
    )

    product = models.ForeignKey(
        Product, 
        related_name="product", 
        on_delete=models.PROTECT
    )

    brand = models.ForeignKey(
        Brand, 
        related_name="brand", 
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    product_attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="product_attribute_values",
        through="ProductAttributeValues"
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name=_("Product visibility"),
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Default selection"),
    )

    retail_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Recommended retail price"),
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    store_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Regular store price"),
    )

    weight = models.FloatField(
        verbose_name=_("Product weight")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Date sub-product created"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date sub-product last updated"),
    )

    users_wishlist = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="user_wishlist", 
        blank=True
    )


    def __str__(self):
        return self.product.name
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
    
    def get_absolute_url(self):
        return reverse("demo:product_detail", kwargs={"slug": self.product.slug})
    
    


class Media(models.Model):

    class Meta:
        verbose_name_plural = _("Product images")


    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.PROTECT,
        related_name="media_product_inventory"
    )

    img_url = models.ImageField(
        upload_to="images/"
    )

    alt_text = models.CharField(
        max_length=255,
        verbose_name=_("Alternative text"),
    )

    is_feature = models.BooleanField(
        default=False,
        verbose_name=_("Product default image"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Date image created"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date image last updated"),
    )



class Stock(models.Model):

    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name="stock_product_inventory",
        on_delete=models.PROTECT
    )

    last_checked = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Inventory stock check date"),
    )

    units = models.IntegerField(
        default=0,
        verbose_name=_("Units/qty of stock"),
    )

    units_sold = models.IntegerField(
        default=0,
        verbose_name=_("Units sold to date"),
    )



class ProductAttributeValues(models.Model):

    class Meta:
        unique_together = (("attribute_values", "product_inventory"))


    attribute_values = models.ForeignKey(
        ProductAttributeValue,
        related_name="attribute_values",
        on_delete=models.PROTECT
    )

    product_inventory = models.ForeignKey(
        ProductInventory,
        related_name="product_inventory",
        on_delete=models.PROTECT
    )



class ProductTypeAttribute(models.Model):

    class Meta:
        unique_together = (("product_attribute", "product_type"))


    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_type_attribute",
        on_delete=models.PROTECT
    )

    product_type = models.ForeignKey(
        ProductType,
        related_name="product_attribute_type",
        on_delete=models.PROTECT
    )