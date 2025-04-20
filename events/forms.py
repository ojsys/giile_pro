from django import forms
from .models import EventRegistration

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['name', 'email', 'phone', 'organization', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mdc-text-field__input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'mdc-text-field__input', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'mdc-text-field__input', 'placeholder': 'Your Phone Number'}),
            'organization': forms.TextInput(attrs={'class': 'mdc-text-field__input', 'placeholder': 'Your Organization'}),
            'message': forms.Textarea(attrs={'class': 'mdc-text-field__input', 'rows': 4, 'placeholder': 'Your Message'}),
        }