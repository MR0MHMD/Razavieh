from django.utils.html import format_html
from django.contrib import admin
from .models import *


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'phone', 'created')
    list_filter = ('created', 'subject')
    search_fields = ('name', 'message')


@admin.register(HeroImage)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "name", "role", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "role")
    list_filter = ("is_active",)
    ordering = ("order",)

    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": ("name", "role", "slug", "is_active")
        }),
        ("تصویر", {
            "fields": ("image", "image_preview")
        }),
        ("تنظیمات نمایش", {
            "fields": ("order",)
        }),
    )

    readonly_fields = ("image_preview",)

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:8px;object-fit:cover;">',
                obj.image.url
            )
        return "—"
    thumbnail.short_description = "تصویر"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" style="border-radius:10px;object-fit:cover;">',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "پیش‌نمایش تصویر"
