from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class AboutPage(models.Model):
    """Model for the About page content."""
    title = models.CharField(_("Page Title"), max_length=100, default="About Giile Pro")
    intro = RichTextField(_("Introduction"), help_text=_("Introductory text at the top of the page"))
    
    # Our Story section
    our_story_title = models.CharField(_("Our Story Title"), max_length=100, default="Our Story")
    our_story = RichTextField(_("Our Story Content"))
    our_story_image = models.ImageField(_("Our Story Image"), upload_to='about/images/', blank=True, null=True)
    
    # Vision section
    vision_title = models.CharField(_("Vision Title"), max_length=100, default="Our Vision")
    vision = RichTextField(_("Vision Content"))
    vision_image = models.ImageField(_("Vision Image"), upload_to='about/images/', blank=True, null=True)
    
    # Mission section
    mission_title = models.CharField(_("Mission Title"), max_length=100, default="Our Mission")
    mission = RichTextField(_("Mission Content"))
    mission_image = models.ImageField(_("Mission Image"), upload_to='about/images/', blank=True, null=True)
    
    # Values section
    values_title = models.CharField(_("Values Title"), max_length=100, default="Our Values")
    
    # Team section
    team_title = models.CharField(_("Team Title"), max_length=100, default="Our Team")
    team_subtitle = RichTextField(_("Team Subtitle"), blank=True)
    
    class Meta:
        verbose_name = _("About Page")
        verbose_name_plural = _("About Pages")
    
    def __str__(self):
        return self.title


class Value(models.Model):
    """Model for individual company values."""
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='values')
    title = models.CharField(_("Value Title"), max_length=100)
    description = RichTextField(_("Value Description"))
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("Value")
        verbose_name_plural = _("Values")
        ordering = ['order']
    
    def __str__(self):
        return self.title


class TeamMember(models.Model):
    """Model for team members displayed on the about page."""
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(_("Name"), max_length=100)
    position = models.CharField(_("Position"), max_length=100)
    bio = RichTextField(_("Biography"))
    photo = models.ImageField(_("Photo"), upload_to='team/photos/', blank=True, null=True)
    linkedin_url = models.URLField(_("LinkedIn URL"), blank=True)
    twitter_url = models.URLField(_("Twitter URL"), blank=True)
    instagram_url = models.URLField(_("Instagram URL"), blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("Team Member")
        verbose_name_plural = _("Team Members")
        ordering = ['order']
    
    def __str__(self):
        return self.name


class SiteSettings(models.Model):
    """Model for site-wide settings."""
    site_title = models.CharField(_("Site Title"), max_length=100, default="Giile Pro")
    site_description = RichTextField(_("Site Description"), blank=True)
    contact_email = models.EmailField(_("Contact Email"), blank=True)
    contact_phone = models.CharField(_("Contact Phone"), max_length=20, blank=True)
    address = RichTextField(_("Address"), blank=True)
    
    # Social media links
    facebook_url = models.URLField(_("Facebook URL"), blank=True)
    twitter_url = models.URLField(_("Twitter URL"), blank=True)
    instagram_url = models.URLField(_("Instagram URL"), blank=True)
    linkedin_url = models.URLField(_("LinkedIn URL"), blank=True)
    youtube_url = models.URLField(_("YouTube URL"), blank=True)
    
    # Footer content
    footer_text = RichTextField(_("Footer Text"), blank=True)
    copyright_text = models.CharField(_("Copyright Text"), max_length=255, blank=True)
    
    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")
    
    def __str__(self):
        return self.site_title
    
    def save(self, *args, **kwargs):
        # Ensure there's only one instance of SiteSettings
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings."""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
