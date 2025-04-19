from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import AboutPage, Value, TeamMember, SiteSettings, HomePage, Service, Event

class ValueInline(admin.StackedInline):
    model = Value
    extra = 1
    classes = ['collapse']

class TeamMemberInline(admin.StackedInline):
    model = TeamMember
    extra = 1
    classes = ['collapse']
    fields = ['name', 'position', 'bio', 'photo', 'preview_photo', 'linkedin_url', 'twitter_url', 'instagram_url', 'order']
    readonly_fields = ['preview_photo']
    
    def preview_photo(self, obj):
        if obj.photo and hasattr(obj.photo, 'url'):
            return format_html('<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 50%;" />', obj.photo.url)
        return "No photo uploaded yet."
    preview_photo.short_description = "Photo Preview"

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'intro')
        }),
        ('Our Story', {
            'fields': ('our_story_title', 'our_story', 'our_story_image'),
            'classes': ('collapse',),
        }),
        ('Vision', {
            'fields': ('vision_title', 'vision', 'vision_image'),
            'classes': ('collapse',),
        }),
        ('Mission', {
            'fields': ('mission_title', 'mission', 'mission_image'),
            'classes': ('collapse',),
        }),
        ('Values Section', {
            'fields': ('values_title',),
            'classes': ('collapse',),
        }),
        ('Team Section', {
            'fields': ('team_title', 'team_subtitle'),
            'classes': ('collapse',),
        }),
    )
    inlines = [ValueInline, TeamMemberInline]
    save_on_top = True
    
    def has_add_permission(self, request):
        # Only allow one instance of AboutPage
        return not AboutPage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deleting the about page
        return False

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_title', 'site_description')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'address'),
            'classes': ('collapse',),
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'),
            'classes': ('collapse',),
        }),
        ('Footer', {
            'fields': ('footer_text', 'copyright_text'),
            'classes': ('collapse',),
        }),
    )
    save_on_top = True
    
    def has_add_permission(self, request):
        # If there's already an instance, don't allow adding
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deleting the site settings
        return False

class ServiceInline(admin.StackedInline):
    model = Service
    extra = 1
    classes = ['collapse']
    fields = ['title', 'description', 'image', 'preview_image', 'button_text', 'button_url', 'order']
    readonly_fields = ['preview_image']
    
    def preview_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" width="200" height="150" style="object-fit: cover;" />', obj.image.url)
        return "No image uploaded yet."
    preview_image.short_description = "Image Preview"

class EventInline(admin.StackedInline):
    model = Event
    extra = 1
    classes = ['collapse']
    fields = ['title', 'date', 'location', 'button_text', 'button_url', 'order']



@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Hero Section'), {
            'fields': ('hero_title', 'hero_subtitle', 'hero_button_text', 'hero_button_url', 'hero_image', 'preview_hero_image')
        }),
        (_('Services Section'), {
            'fields': ('services_title',)
        }),
        (_('Events Section'), {
            'fields': ('events_title', 'events_button_text', 'events_button_url')
        }),
        (_('Blog Section'), {
            'fields': ('blog_title', 'blog_button_text', 'blog_button_url')
        }),
    )
    readonly_fields = ['preview_hero_image']
    inlines = [ServiceInline, EventInline]
    save_on_top = True
    
    def preview_hero_image(self, obj):
        if obj.hero_image and hasattr(obj.hero_image, 'url'):
            return format_html('<img src="{}" width="400" height="200" style="object-fit: cover;" />', obj.hero_image.url)
        return "No hero image uploaded yet."
    preview_hero_image.short_description = "Hero Image Preview"
    
    def has_add_permission(self, request):
        # Only allow one instance of HomePage
        return not HomePage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deleting the home page
        return False

# Add these registrations at the end of your admin.py file
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'home_page', 'order']
    list_filter = ['home_page']
    search_fields = ['title', 'description']
    fields = ['home_page', 'title', 'description', 'image', 'preview_image', 'button_text', 'button_url', 'order']
    readonly_fields = ['preview_image']
    
    def preview_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" width="200" height="150" style="object-fit: cover;" />', obj.image.url)
        return "No image uploaded yet."
    preview_image.short_description = "Image Preview"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'home_page', 'order']
    list_filter = ['home_page']
    search_fields = ['title', 'date', 'location']
    fields = ['home_page', 'title', 'date', 'location', 'button_text', 'button_url', 'order']


