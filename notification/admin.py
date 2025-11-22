from django.contrib import admin
from .models import *


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'content')
    list_editable = ['is_active']
    autocomplete_fields = ['tags']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'notification_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ("اطلاعات برچسب", {"fields": ("name", "slug")}),
    )

    def notification_count(self, obj):
        return obj.notification.count()

    notification_count.short_description = "تعداد اطلاع رسانی ها"
