from django.contrib import admin
from .models import DonationCard


@admin.register(DonationCard)
class DonationCardAdmin(admin.ModelAdmin):
    list_display = ("title", "card_number", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "card_number")
    list_editable = ["is_active"]
