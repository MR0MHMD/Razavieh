from django_jalali.admin.filters import JDateFieldListFilter
from blog.models import Post, Comment
from django.contrib import admin


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['name', 'body']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created')
    search_fields = ('title', 'slug')
    # prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    ordering = ('-created',)
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'created', 'active')
    list_filter = ('active', ('created', JDateFieldListFilter))
    search_fields = ('name', 'body')
    list_editable = ('active',)
