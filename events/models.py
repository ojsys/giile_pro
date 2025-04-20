from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField

class EventCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, max_length=100)
    
    class Meta:
        verbose_name = _("Event Category")
        verbose_name_plural = _("Event Categories")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('events:category', args=[self.slug])

class Event(models.Model):
    STATUS_CHOICES = (
        ('upcoming', _('Upcoming')),
        ('ongoing', _('Ongoing')),
        ('past', _('Past')),
        ('cancelled', _('Cancelled')),
    )
    
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, max_length=200)
    featured_image = models.ImageField(_("Featured Image"), upload_to='events/images/', blank=True, null=True)
    short_description = models.TextField(_("Short Description"), help_text=_("A brief description of the event"))
    content = RichTextField(_("Content"), help_text=_("Detailed description of the event"))
    
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"), blank=True, null=True)
    location = models.CharField(_("Location"), max_length=255)
    venue = models.CharField(_("Venue"), max_length=255, blank=True)
    address = models.TextField(_("Address"), blank=True)
    google_map_link = models.URLField(_("Google Map Link"), max_length=400, blank=True)
    
    registration_url = models.URLField(_("Registration URL"), blank=True)
    registration_deadline = models.DateTimeField(_("Registration Deadline"), blank=True, null=True)
    
    categories = models.ManyToManyField(EventCategory, related_name='events', verbose_name=_("Categories"), blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='upcoming')
    
    is_featured = models.BooleanField(_("Featured Event"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ['start_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('events:event_detail', args=[self.slug])
    
    @property
    def formatted_date(self):
        """Return a formatted date string for display"""
        if self.end_date:
            if self.start_date.date() == self.end_date.date():
                # Same day event
                return f"{self.start_date.strftime('%B %d, %Y')} | {self.start_date.strftime('%I:%M %p')} - {self.end_date.strftime('%I:%M %p')}"
            else:
                # Multi-day event
                return f"{self.start_date.strftime('%B %d')} - {self.end_date.strftime('%B %d, %Y')}"
        return self.start_date.strftime("%B %d, %Y | %I:%M %p")
    
    @property
    def is_past(self):
        """Check if the event is in the past"""
        from django.utils import timezone
        end = self.end_date if self.end_date else self.start_date
        return end < timezone.now()

class EventSpeaker(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='speakers', verbose_name=_("Event"))
    name = models.CharField(_("Name"), max_length=100)
    title = models.CharField(_("Title/Position"), max_length=100, blank=True)
    bio = models.TextField(_("Biography"), blank=True)
    photo = models.ImageField(_("Photo"), upload_to='events/speakers/', blank=True, null=True)
    website = models.URLField(_("Website"), blank=True)
    
    class Meta:
        verbose_name = _("Event Speaker")
        verbose_name_plural = _("Event Speakers")
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations', verbose_name=_("Event"))
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    organization = models.CharField(_("Organization"), max_length=100, blank=True)
    message = models.TextField(_("Message"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Event Registration")
        verbose_name_plural = _("Event Registrations")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"
