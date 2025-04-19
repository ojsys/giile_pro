from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class User(AbstractUser):
    """
    Custom user model for enhanced user functionality.
    Extends Django's AbstractUser to allow for comprehensive user profiles.
    """
    # Contact Information
    email = models.EmailField(_('email address'), unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Profile Information
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Address Information
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Social Media
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    
    # Account Settings
    email_verified = models.BooleanField(default=False)
    receive_newsletter = models.BooleanField(default=True)
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    # User Type - for different types of users in the system
    USER_TYPE_CHOICES = (
        ('regular', 'Regular User'),
        ('artist', 'Artist'),
        ('manager', 'Manager'),
        ('admin', 'Administrator'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='regular')
    
    # Make email required
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    def get_profile_completion_percentage(self):
        """
        Calculate how complete the user's profile is.
        """
        fields = [
            self.first_name, self.last_name, self.email, self.phone_number,
            self.bio, self.profile_picture, self.date_of_birth,
            self.address_line1, self.city, self.state, self.postal_code, self.country
        ]
        
        filled_fields = sum(1 for field in fields if field)
        return int((filled_fields / len(fields)) * 100)
