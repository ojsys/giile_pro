from django.contrib import admin
from django.utils.html import format_html
from .models import TalentCategory, Skill, Talent, PortfolioItem, Testimonial, BookingRequest

@admin.register(TalentCategory)
class TalentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

class PortfolioItemInline(admin.TabularInline):
    model = PortfolioItem
    extra = 1
    fields = ['title', 'image', 'video_url', 'project_date', 'client', 'order']

class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1
    fields = ['client_name', 'client_position', 'client_company', 'content', 'rating', 'date']

@admin.register(Talent)
class TalentAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_categories', 'years_of_experience', 'status', 'is_featured', 'preview_image']
    list_filter = ['status', 'is_featured', 'categories', 'skills']
    search_fields = ['name', 'short_bio', 'biography', 'email', 'phone']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['categories', 'skills']
    inlines = [PortfolioItemInline, TestimonialInline]
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'status', 'is_featured')
        }),
        ('Images', {
            'fields': ('profile_image', 'preview_image', 'cover_image')
        }),
        ('Personal Information', {
            'fields': ('gender', 'date_of_birth', 'short_bio', 'biography')
        }),
        ('Professional Information', {
            'fields': ('categories', 'skills', 'years_of_experience', 'hourly_rate')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Social Media', {
            'fields': ('instagram', 'twitter', 'facebook', 'linkedin', 'youtube'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['preview_image']
    
    def preview_image(self, obj):
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 50%;" />', obj.profile_image.url)
        return "No image uploaded yet."
    preview_image.short_description = "Profile Image Preview"
    
    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = "Categories"

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'talent', 'project_date', 'client', 'order']
    list_filter = ['talent', 'project_date']
    search_fields = ['title', 'description', 'client', 'talent__name']
    ordering = ['talent', 'order', '-project_date']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'talent', 'client_company', 'rating', 'date']
    list_filter = ['talent', 'rating', 'date']
    search_fields = ['client_name', 'client_company', 'content', 'talent__name']

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ['project_title', 'talent', 'client_name', 'start_date', 'status', 'created_at']
    list_filter = ['status', 'start_date', 'talent']
    search_fields = ['project_title', 'client_name', 'client_email', 'client_company', 'talent__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('talent', 'status', 'project_title')
        }),
        ('Client Information', {
            'fields': ('client_name', 'client_email', 'client_phone', 'client_company')
        }),
        ('Project Details', {
            'fields': ('project_description', 'start_date', 'end_date', 'budget')
        }),
        ('Administrative', {
            'fields': ('admin_notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
