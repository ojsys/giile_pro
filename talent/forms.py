from django import forms
from .models import Talent, BookingRequest, PortfolioItem, Testimonial, Availability

class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = [
            'client_name', 'client_email', 'client_phone', 'client_company',
            'project_title', 'project_description', 'start_date', 'end_date', 'budget'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'project_description': forms.Textarea(attrs={'rows': 4}),
        }

class TalentProfileForm(forms.ModelForm):
    class Meta:
        model = Talent
        fields = [
            'name', 'short_bio', 'biography', 'profile_image', 'cover_image',
            'years_of_experience', 'hourly_rate', 'location', 'categories', 'skills',
            'website', 'instagram', 'twitter', 'facebook', 'linkedin', 'youtube',
            'email', 'phone', 'show_availability'
        ]
        widgets = {
            'short_bio': forms.Textarea(attrs={'rows': 3}),
            'biography': forms.Textarea(attrs={'rows': 8}),
            'categories': forms.CheckboxSelectMultiple(),
            'skills': forms.CheckboxSelectMultiple(),
        }

class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = [
            'title', 'description', 'image', 'video_url', 'client', 
            'project_date', 'order'
        ]
        widgets = {
            'project_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = [
            'client_name', 'client_position', 'client_company', 'client_image',
            'content', 'rating', 'date'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['date', 'is_available']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }