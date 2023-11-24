from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User as DefaultUser

# Register your models here.
from .models import Subscription, TgUser


class User(DefaultUser):
    class Meta:
        proxy = True
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'


admin.site.unregister(DefaultUser)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')


class TgUserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'user_name')


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(TgUser, TgUserAdmin)
