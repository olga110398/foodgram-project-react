from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
