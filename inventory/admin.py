from django.contrib import admin
from inventory.models import *


@admin.register(Scrotter)
class ScrotterAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'quantity', 'width')
    list_filter = ('category', 'width')
    search_fields = ('text', 'category')


@admin.register(Decorative)
class DecorativeAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    search_fields = ('name', 'description')
