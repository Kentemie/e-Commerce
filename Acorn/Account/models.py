import uuid

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django_countries.fields import CountryField



class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **other_fields):
        other_fields.setdefault("is_staff", False)
        other_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **other_fields)

    def create_superuser(self, username, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self._create_user(username, email, password, **other_fields)
    
    def _create_user(self, username, email, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()

        return user



class UserModel(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    info_about = models.TextField(_("Some information about the user."), blank=True)

    # Delivery information
    delivery_info = models.BooleanField(_("Saved order information."), default=False)

    # User status
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'admin@gmail.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.username



class UserAddress(models.Model):

    class Meta:
        verbose_name = _("User address")
        verbose_name_plural = _("User addresses")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="addresses")
    country = CountryField(blank_label="(select country)")
    city = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=12)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150, blank=True, null=True)
    delivery_instructions = models.CharField(max_length=255, blank=True, null=True)
    is_main = models.BooleanField(default=False)

    phone_number_1 = models.CharField(max_length=15)
    phone_number_2 = models.CharField(max_length=15, blank=True, null=True)

    
    def __str__(self):
        return f"{self.country}, {self.city}, {self.address_line_1}"
    
    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except MultipleObjectsReturned as e:
            raise e
        except ObjectDoesNotExist:
            return None

