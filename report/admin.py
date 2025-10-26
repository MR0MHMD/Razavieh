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
class ResizedImageFieldAdmin(admin.ModelAdmin):
    list_display = ['report']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('report', 'name', 'created', 'active')
    list_filter = ('active', ('created', JDateFieldListFilter))
    search_fields = ('name', 'body')
    list_editable = ['active']


@admin.register(ReportLike)
class ReportLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'user')
    list_filter = ('report',)
    search_fields = ('report__title', 'user__username')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'views', 'likes')
    search_fields = ('title', 'description')
    list_filter = ('date', 'categories')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    fieldsets = (
        ('اطلاعات کلی', {'fields': ('title', 'slug', 'description', 'date')}),
        ('تگ‌ها و آمار', {'fields': ('tags', 'likes', 'views', 'categories')}),
    )
