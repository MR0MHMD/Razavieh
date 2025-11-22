from django_jalali.admin.filters import JDateFieldListFilter
from django.contrib import admin
from report.models import *


class inlines:
    class ImageInline(admin.TabularInline):
        model = ReportImage
        extra = 0

    class CommentInline(admin.TabularInline):
        model = Comment
        extra = 0
        readonly_fields = ['name', 'body']

    class LikeInline(admin.TabularInline):
        model = ReportLike
        extra = 0
        readonly_fields = ['report', 'user']


@admin.register(ReportImage)
class ReportImagedAdmin(admin.ModelAdmin):
    list_display = ['report']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'report_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ("اطلاعات برچسب", {"fields": ("name", "slug")}),
        ("تنظیمات سئو", {"fields": ("seo_title", "seo_description")}),
    )

    def report_count(self, obj):
        return obj.reports.count()

    report_count.short_description = "تعداد گزارش‌ها"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('report', 'name', 'created', 'active')
    list_filter = ('active', ('created', JDateFieldListFilter))
    search_fields = ('name', 'body')
    list_editable = ['active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_display = ('name', 'report_count')

    fieldsets = (
        ("اطلاعات دسته", {"fields": ("name", "slug")}),
        ("تنظیمات سئو", {"fields": ("seo_title", "seo_description")}),
    )

    def report_count(self, obj):
        return obj.reports.count()

    report_count.short_description = "تعداد گزارش‌ها"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'views', 'likes')
    search_fields = ('title', 'description')
    list_filter = ('date', 'categories')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'

    autocomplete_fields = ['tags', 'categories']

    inlines = [inlines.ImageInline, inlines.CommentInline, inlines.LikeInline]

    fieldsets = (
        ('اطلاعات کلی', {'fields': ('title', 'slug', 'description', 'date')}),
        ('تگ‌ها و آمار', {'fields': ('tags', 'likes', 'views', 'categories')}),
    )
