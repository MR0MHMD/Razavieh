from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {'fields': ('photo', 'date_of_birth', 'bio')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
