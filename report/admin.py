from django.contrib import admin

from report.models import Report, ReportImage


# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(ReportImage)
class ResizedImageFieldAdmin(admin.ModelAdmin):
    list_display = ['report']
