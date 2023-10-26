from django.contrib import admin

from .models import UserModel, UserAddress

admin.site.register(UserModel)
admin.site.register(UserAddress)