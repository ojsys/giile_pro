from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['name', 'email', 'content', 'active']
    readonly_fields = ['name', 'email', 'content']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'published_at', 'preview_image']
    list_filter = ['status', 'created_at', 'published_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    filter_horizontal = ['categories', 'tags']
    inlines = [CommentInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('Content', {
            'fields': ('excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image', 'preview_image')
        }),
        ('Categories & Tags', {
            'fields': ('categories', 'tags')
        }),
        ('Publication', {
            'fields': ('published_at',)
        }),
    )
    readonly_fields = ['preview_image']
    
    def preview_image(self, obj):
        if obj.featured_image and hasattr(obj.featured_image, 'url'):
            return format_html('<img src="{}" width="150" height="100" style="object-fit: cover;" />', obj.featured_image.url)
        return "No image uploaded yet."
    preview_image.short_description = "Featured Image Preview"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_at', 'active']
    list_filter = ['active', 'created_at']
    search_fields = ['name', 'email', 'content']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)
    disapprove_comments.short_description = "Disapprove selected comments"
