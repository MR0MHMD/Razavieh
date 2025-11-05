from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime', 'is_active')
    list_filter = ('is_active', 'datetime')
    search_fields = ('title', 'content')
    list_editable = ['is_active']
