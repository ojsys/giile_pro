from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User 
from django.conf import settings

class TalentCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, max_length=100)
    description = models.TextField(_("Description"), blank=True)
    
    class Meta:
        verbose_name = _("Talent Category")
        verbose_name_plural = _("Talent Categories")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('talent:category', args=[self.slug])

class Skill(models.Model):
    name = models.CharField(_("Skill Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, max_length=100)
    
    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Talent(models.Model):
    # Add this field to link talents to users
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='talent_profile', null=True, blank=True)
    
    GENDER_CHOICES = (
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    )
    
    STATUS_CHOICES = (
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('featured', _('Featured')),
    )
    
    name = models.CharField(_("Full Name"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, max_length=200)
    profile_image = models.ImageField(_("Profile Image"), upload_to='talents/profile/', blank=True, null=True)
    cover_image = models.ImageField(_("Cover Image"), upload_to='talents/cover/', blank=True, null=True)
    
    gender = models.CharField(_("Gender"), max_length=10, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    
    short_bio = models.TextField(_("Short Bio"), help_text=_("A brief introduction (max 200 words)"))
    biography = RichTextField(_("Biography"), blank=True)
    
    categories = models.ManyToManyField(TalentCategory, related_name='talents', verbose_name=_("Categories"))
    skills = models.ManyToManyField(Skill, related_name='talents', verbose_name=_("Skills"), blank=True)
    
    years_of_experience = models.PositiveIntegerField(_("Years of Experience"), default=0)
    hourly_rate = models.DecimalField(_("Hourly Rate"), max_digits=10, decimal_places=2, blank=True, null=True)
    
    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    website = models.URLField(_("Website"), blank=True)
    
    location = models.CharField(max_length=100, blank=True)
    show_availability = models.BooleanField(default=False)
    
    # Social media links
    instagram = models.URLField(_("Instagram"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    facebook = models.URLField(_("Facebook"), blank=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True)
    youtube = models.URLField(_("YouTube"), blank=True)
    
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(_("Featured"), default=False)
    
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Talent")
        verbose_name_plural = _("Talents")
        ordering = ['-is_featured', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('talent:talent_detail', args=[self.slug])
    
    @property
    def age(self):
        """Calculate age based on date of birth"""
        if not self.date_of_birth:
            return None
        from django.utils import timezone
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    # Add these new fields
    

class PortfolioItem(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='portfolio_items', verbose_name=_("Talent"))
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(_("Image"), upload_to='talents/portfolio/', blank=True, null=True)
    video_url = models.URLField(_("Video URL"), blank=True, help_text=_("YouTube or Vimeo URL"))
    project_date = models.DateField(_("Project Date"), blank=True, null=True)
    client = models.CharField(_("Client"), max_length=200, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("Portfolio Item")
        verbose_name_plural = _("Portfolio Items")
        ordering = ['order', '-project_date']
    
    def __str__(self):
        return f"{self.title} - {self.talent.name}"

class Testimonial(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='testimonials', verbose_name=_("Talent"))
    client_name = models.CharField(_("Client Name"), max_length=100)
    client_position = models.CharField(_("Client Position"), max_length=100, blank=True)
    client_company = models.CharField(_("Client Company"), max_length=100, blank=True)
    client_image = models.ImageField(_("Client Image"), upload_to='talents/testimonials/', blank=True, null=True)
    content = models.TextField(_("Testimonial Content"))
    rating = models.PositiveSmallIntegerField(_("Rating"), choices=[(i, i) for i in range(1, 6)], default=5)
    date = models.DateField(_("Date"), blank=True, null=True)
    
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.client_name} - {self.talent.name}"

class BookingRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )
    
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='booking_requests', verbose_name=_("Talent"))
    client_name = models.CharField(_("Client Name"), max_length=100)
    client_email = models.EmailField(_("Client Email"))
    client_phone = models.CharField(_("Client Phone"), max_length=20, blank=True)
    client_company = models.CharField(_("Client Company"), max_length=100, blank=True)
    
    project_title = models.CharField(_("Project Title"), max_length=200)
    project_description = models.TextField(_("Project Description"))
    
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"), blank=True, null=True)
    
    budget = models.DecimalField(_("Budget"), max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    admin_notes = models.TextField(_("Admin Notes"), blank=True, help_text=_("Notes visible only to administrators"))
    
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Booking Request")
        verbose_name_plural = _("Booking Requests")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.talent.name} - {self.project_title}"


class Availability(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='availability_dates')
    date = models.DateField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Availability Date'
        verbose_name_plural = 'Availability Dates'
        unique_together = ('talent', 'date')
        ordering = ['date']
    
    def __str__(self):
        status = "Available" if self.is_available else "Not Available"
        return f"{self.talent.name} - {self.date} - {status}"
