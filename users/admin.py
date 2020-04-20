from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class NegotiatorAdmin(UserAdmin):
    list_display = ('guid', 'username', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'last_request_at')  # noqa
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')
    list_editable = ['is_staff', 'is_superuser', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('last_request_at',)}),
    )
