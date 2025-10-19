from django_jalali.admin.filters import JDateFieldListFilter
from report.models import *
from django.contrib import admin


class inlines:
    class ImageInline(admin.TabularInline):
        model = ReportImage
        extra = 0

    class CommentInline(admin.TabularInline):
        model = Comment
        extra = 0
        readonly_fields = ['name', 'body']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [inlines.ImageInline, inlines.CommentInline]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ReportImage)
class ResizedImageFieldAdmin(admin.ModelAdmin):
    list_display = ['report']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('report', 'name', 'created', 'active')
    list_filter = ('active', ('created', JDateFieldListFilter))
    search_fields = ('name', 'body')
    list_editable = ['active']
