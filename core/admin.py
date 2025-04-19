from django.contrib import admin
from django.utils.html import format_html
from .models import AboutPage, Value, TeamMember, SiteSettings

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
