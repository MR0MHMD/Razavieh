from django_jalali.admin.filters import JDateFieldListFilter
from django.utils.html import format_html
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

    class VideoInline(admin.TabularInline):
        model = ReportVideo
        extra = 0
        readonly_fields = ['title', 'video_uid', "description"]

    class AudioInline(admin.TabularInline):
        model = ReportAudio
        extra = 2
        fields = ("title", "audio_url", "description")
        show_change_link = True


@admin.register(ReportImage)
class ReportImagedAdmin(admin.ModelAdmin):
    list_display = ['report']


@admin.register(ReportVideo)
class ReportVideoAdmin(admin.ModelAdmin):
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

    inlines = [inlines.ImageInline, inlines.CommentInline, inlines.LikeInline, inlines.VideoInline, inlines.AudioInline]

    fieldsets = (
        ('اطلاعات کلی', {'fields': ('title', 'slug', 'description', 'date')}),
        ('تگ‌ها و آمار', {'fields': ('tags', 'likes', 'views', 'categories')}),
    )


@admin.register(ReportAudio)
class ReportAudioAdmin(admin.ModelAdmin):
    list_display = ("title", "report", "created", "player_mini")
    search_fields = ("title", "description", "audio_url")
    list_filter = ("created", "report")
    ordering = ("-created",)

    fields = ("report", "title", "audio_url", "description", "player_mini")
    readonly_fields = ("player_mini",)

    def player_mini(self, obj):
        if not obj.audio_url:
            return "-"
        return format_html(
            '''
            <audio controls style="width: 150px; height: 30px;">
                <source src="{}" type="audio/mpeg">
            </audio>
            ''',
            obj.audio_url
        )
    player_mini.short_description = "پیش‌نمایش صوت"
