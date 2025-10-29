from django.contrib import admin
from .models import *
import Razavieh


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'phone', 'created')
    list_filter = ('created', 'subject')
    search_fields = ('name', 'message')
