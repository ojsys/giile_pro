from django.contrib import admin
from django.utils.html import format_html
from .models import EventCategory, Event, EventSpeaker, EventRegistration

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

class EventSpeakerInline(admin.TabularInline):
    model = EventSpeaker
    extra = 1

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ['name', 'email', 'phone', 'organization', 'message', 'created_at']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'location', 'status', 'is_featured', 'preview_image']
    list_filter = ['status', 'is_featured', 'start_date', 'categories']
    search_fields = ['title', 'short_description', 'content', 'location', 'venue']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    filter_horizontal = ['categories']
    inlines = [EventSpeakerInline, EventRegistrationInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'is_featured')
        }),
        ('Content', {
            'fields': ('short_description', 'content')
        }),
        ('Media', {
            'fields': ('featured_image', 'preview_image')
        }),
        ('Date & Location', {
            'fields': ('start_date', 'end_date', 'location', 'venue', 'address', 'google_map_link')
        }),
        ('Registration', {
            'fields': ('registration_url', 'registration_deadline')
        }),
        ('Categories', {
            'fields': ('categories',)
        }),
    )
    readonly_fields = ['preview_image']
    
    def preview_image(self, obj):
        if obj.featured_image and hasattr(obj.featured_image, 'url'):
            return format_html('<img src="{}" width="150" height="100" style="object-fit: cover;" />', obj.featured_image.url)
        return "No image uploaded yet."
    preview_image.short_description = "Featured Image Preview"

@admin.register(EventSpeaker)
class EventSpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'event']
    list_filter = ['event']
    search_fields = ['name', 'title', 'bio']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'event', 'created_at']
    list_filter = ['event', 'created_at']
    search_fields = ['name', 'email', 'phone', 'organization']
    readonly_fields = ['created_at']
